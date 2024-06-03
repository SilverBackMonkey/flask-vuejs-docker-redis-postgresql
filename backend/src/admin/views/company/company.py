from flask import request, redirect, flash

from companies.models import Company, CEO, Financial
from companies.types import FinancialSource
from companies.tasks import retrieve_company, retrieve_financials
from companies.repository import CompanyRepository, CEORepository, FinancialRepository

from flask_admin import expose
from flask_admin.form.fields import Select2TagsField, Select2Field
from flask_admin.form import SecureForm
from flask_admin.babel import gettext, ngettext

from core.fields import AdminImageUploadField
from core.admin import register_view, AdminModelView

from wtforms.fields import IntegerField, StringField, FloatField, SelectField
from wtforms.validators import InputRequired, NumberRange, Optional

from pathlib import Path
from os.path import splitext
from datetime import datetime


class CeoForm(SecureForm):
    full_name = StringField(label="Full Name", validators=[InputRequired()])
    start_year = IntegerField(label="Start Year", validators=[
        InputRequired(),
        NumberRange(
            min=1000,
            max=9000
        )
    ])
    end_year = IntegerField(label="End Year", validators=[
        NumberRange(
            min=1000,
            max=9000
        ),
        Optional()
    ])


class FinancialForm(SecureForm):
    year = IntegerField(label="Year", validators=[
        InputRequired(),
        NumberRange(
            min=1000,
            max=9000
        )
    ])
    quarter = IntegerField(label="Quarter", validators=[
        NumberRange(
            min=1,
            max=4
        ),
        Optional()
    ])
    source = SelectField(
        choices=[
            (FinancialSource.IEXCLOUD.name, FinancialSource.IEXCLOUD.name),
            (FinancialSource.POLYGONIO.name, FinancialSource.POLYGONIO.name),
            (FinancialSource.CUSTOM.name, FinancialSource.CUSTOM.name),
        ],
        label="Financial Source",
    )
    net_income = IntegerField(label="Net Income")
    shares_outstanding = IntegerField(label="Shares Outstanding")
    free_cash_flow = FloatField(label="Free Cash Flow")
    cash_flow_from_operating_activities = FloatField(label="Cash Flow From Operating Activities")
    dividends_per_share = FloatField(label="Dividends Per Share")
    revenue = IntegerField(label="Revenue")
    capex = IntegerField(label="Capex")
    total_assets = IntegerField(label="Total Assets")
    total_liabilities = IntegerField(label="Total Liabilities")
    net_debt = IntegerField(label="Net Debt")
    interest_coverage = FloatField(label="Interest Coverage")
    dividend_yield = FloatField(label="Dividend Yield")
    min_stock_price = FloatField(label="Min Stock Price")
    max_stock_price = FloatField(label="Max Stock Price")
    price_earnings_ratio_ltm = FloatField(label="Price Earnings Ratio LTM")
    # previous: 'Financial'



def generate_image_name(obj, file_data):
    parts = splitext(file_data.filename)
    return '{}_{}{}'.format(datetime.now().timestamp(), parts[0], parts[1])


@register_view(Company)
class CompanyView(AdminModelView):
    edit_template = "company_edit_template.html"
    create_template = "company_create_template.html"
    column_list = ('symbol', 'name')

    form_overrides = {
        'keywords': Select2TagsField,
        "data_source": Select2Field,
        "founded": IntegerField,
        "logo": AdminImageUploadField
    }

    column_descriptions = {
        "short_name": "If this field is left empty, it will be downloaded from a financial source",
        "employees": "If this field is left empty, it will be downloaded from a financial source",
        "summary": "If this field is left empty, it will be downloaded from a financial source"
    }

    form_args = {
        "keywords": {
            "render_kw": {
                "style": "width:100%!important;"
            }
        },
        'data_source': {
            "choices": [
                (FinancialSource.IEXCLOUD.name, FinancialSource.IEXCLOUD.name),
                (FinancialSource.CUSTOM.name, FinancialSource.CUSTOM.name),
            ],
            "coerce": str,
            "render_kw": {
                "style": "width:100%!important;"
            },
        },
        "founded": {
            "validators": [
                InputRequired(),
                NumberRange(
                    min=1000,
                    max=9000
                )
            ]
        },
        "logo": {
            "url_relative_path": "/companies/img/",
            "endpoint": "/files",
            "namegen": generate_image_name,
            "base_path": Path(__file__).parent.parent.parent.joinpath("static/companies/img")
        }
    }

    def after_model_change(self, form, model, is_created):
        if not is_created:
            return

        retrieve_company.delay(symbol=model.symbol)
        retrieve_financials.delay(symbol=model.symbol)

    @expose('/sync/<int:id>/', methods=["POST"])
    def sync(self, id):
        repository = CompanyRepository(sync=True)
        company = repository.find_one(id=id)

        if company is None:
            return "Company not found!"

        retrieve_company.delay(symbol=company.symbol)
        retrieve_financials.delay(symbol=company.symbol)

        return "Success"

    @expose('/<int:id>/ceo', methods=["GET"])
    def ceo_list(self, id):
        company_repository = CompanyRepository(sync=True)
        company: Company = company_repository.find_one(id=id)

        if company is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(f"/admin/company")

        company_ceo_repository = CEORepository(sync=True)
        ceo = company_ceo_repository.find_all(company_id=company.id)

        return self.render(
            "company_ceo_list_template.html",
            company=company,
            return_url="/admin/company/",
            num_pages=0,
            ceo=ceo,
            ceo_keys=CEO.__annotations__.keys(),
            include_ceo_keys=("full_name", "start_year", "end_year")
        )

    @expose('/<int:id>/ceo/create', methods=["GET", "POST"])
    def ceo_create(self, id):
        form = CeoForm(request.form)

        company_repository = CompanyRepository(sync=True)
        company: Company = company_repository.find_one(id=id)

        if company is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(f"/admin/company")

        if request.method == "GET" or not form.validate():
            return self.render(
                "company_ceo_create_template.html",
                form=form,
                company=company,
                return_url="/admin/company/"
            )

        company_ceo_repository = CEORepository(sync=True)

        if form.end_year.data is None:
            company_ceo = company_ceo_repository.find_one(
                company_id=company.id,
                end_year=None
            )
            if company_ceo:
                form.end_year.errors.append(
                    "Invalid field"
                )

                return self.render(
                    "company_ceo_create_template.html",
                    form=form,
                    company=company,
                    return_url="/admin/company/"
                )

        ceo = company_ceo_repository.create(
            company_id=company.id,
            full_name=form.full_name.data,
            start_year=form.start_year.data,
            end_year=form.end_year.data
        )

        if '_add_another' in request.form:
            return redirect(f"/admin/company/{company.id}/ceo/create")
        elif '_continue_editing' in request.form:
            return redirect(f"/admin/company/{company.id}/ceo/{ceo.id}/edit")
        else:
            flash(gettext('Record was successfully created.'), 'success')
            return redirect(f"/admin/company/{company.id}/ceo")

    @expose('/<int:id>/ceo/<int:ceo_id>/edit', methods=["GET", "POST"])
    def ceo_edit(self, id, ceo_id):
        form = CeoForm(request.form)

        company_repository = CompanyRepository(sync=True)
        company: Company = company_repository.find_one(id=id)

        if company is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(f"/admin/company")

        company_ceo_repository = CEORepository(sync=True)
        ceo: CEO = company_ceo_repository.find_one(id=ceo_id, company_id=company.id)

        if ceo is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(f"/admin/company/{company.id}/ceo")

        if request.method == "GET" or not form.validate():
            form.full_name.data = ceo.full_name
            form.start_year.data = ceo.start_year
            form.end_year.data = ceo.end_year

            return self.render(
                "company_ceo_edit_template.html",
                form=form,
                company=company,
                ceo=ceo,
                return_url="/admin/company/"
            )

        ceo.full_name = form.full_name.data
        ceo.start_year = form.start_year.data
        ceo.end_year = form.end_year.data

        company_ceo_repository.save(ceo)

        if '_add_another' in request.form:
            return redirect(f"/admin/company/{company.id}/ceo/create")
        elif '_continue_editing' in request.form:
            return redirect(f"/admin/company/{company.id}/ceo/{ceo.id}/edit")
        else:
            flash(gettext('Record was successfully saved.'), 'success')
            return redirect(f"/admin/company/{company.id}/ceo")

    @expose('/<int:id>/ceo/<int:ceo_id>/delete', methods=["POST"])
    def ceo_delete(self, id, ceo_id):
        company_repository = CompanyRepository(sync=True)
        company: Company = company_repository.find_one(id=id)

        if company is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(f"/admin/company")

        company_ceo_repository = CEORepository(sync=True)
        ceo: CEO = company_ceo_repository.find_one(id=ceo_id, company_id=company.id)

        if ceo is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(f"/admin/company/{company.id}/ceo")

        company_ceo_repository.delete(ceo)

        count = 1
        flash(
            ngettext(
                'Record was successfully deleted.',
                '%(count)s records were successfully deleted.',
                count, count=count
            ),
            'success'
        )
        return redirect(f"/admin/company/{company.id}/ceo")

    @expose('/<int:id>/financial', methods=["GET"])
    def financial_list(self, id):
        company_repository = CompanyRepository(sync=True)
        company: Company = company_repository.find_one(id=id)

        if company is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(f"/admin/company")

        company_financial_repository = FinancialRepository(sync=True)
        financial = company_financial_repository.find_all(company_id=company.id)

        return self.render(
            "company_financial_list_template.html",
            company=company,
            return_url="/admin/company/",
            num_pages=0,
            financial=financial,
            financial_keys=Financial.__annotations__.keys(),
            include_financial_keys=("year", "quarter", "source")
        )


    @expose('/<int:id>/financial/create', methods=["GET", "POST"])
    def financial_create(self, id):
        form = FinancialForm(request.form)

        company_repository = CompanyRepository(sync=True)
        company: Company = company_repository.find_one(id=id)

        if company is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(f"/admin/company")

        if request.method == "GET" or not form.validate():
            form.source.choices = [
                (FinancialSource.CUSTOM.name, FinancialSource.CUSTOM.name),
            ]

            return self.render(
                "company_financial_create_template.html",
                form=form,
                company=company,
                return_url="/admin/company/"
            )

        company_financial_repository = FinancialRepository(sync=True)

        # if form.year.data is None:
        #     company_financial = company_financial_repository.find_one(
        #         company_id=company.id,
        #         # end_year=None
        #     )
        #     if company_financial:
        #         form.end_year.errors.append(
        #             "Invalid field"
        #         )
        #
        #         return self.render(
        #             "company_financial_create_template.html",
        #             form=form,
        #             company=company,
        #             return_url="/admin/company/"
        #         )

        financial = company_financial_repository.create(
            company_id=company.id,
            source=form.source.data,
            year=form.year.data,
            quarter=form.quarter.data,
            net_income=form.net_income.data,
            shares_outstanding=form.shares_outstanding.data,
            free_cash_flow=form.free_cash_flow.data,
            cash_flow_from_operating_activities=form.cash_flow_from_operating_activities.data,
            dividends_per_share=form.dividends_per_share.data,
            revenue=form.revenue.data,
            capex=form.capex.data,
            total_assets=form.total_assets.data,
            total_liabilities=form.total_liabilities.data,
            net_debt=form.net_debt.data,
            interest_coverage=form.interest_coverage.data,
            dividend_yield=form.dividend_yield.data,
            min_stock_price=form.min_stock_price.data,
            max_stock_price=form.max_stock_price.data,
            price_earnings_ratio_ltm=form.price_earnings_ratio_ltm.data
        )

        if '_add_another' in request.form:
            return redirect(f"/admin/company/{company.id}/financial/create")
        elif '_continue_editing' in request.form:
            return redirect(f"/admin/company/{company.id}/financial/{financial.id}/edit")
        else:
            flash(gettext('Record was successfully created.'), 'success')
            return redirect(f"/admin/company/{company.id}/financial")

    @expose('/<int:id>/financial/<int:financial_id>/edit', methods=["GET", "POST"])
    def financial_edit(self, id, financial_id):
        form = FinancialForm(request.form)

        company_repository = CompanyRepository(sync=True)
        company: Company = company_repository.find_one(id=id)

        if company is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(f"/admin/company")

        company_financial_repository = FinancialRepository(sync=True)
        financial: Financial = company_financial_repository.find_one(id=financial_id, company_id=company.id)

        if financial is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(f"/admin/company/{company.id}/financial")

        if request.method == "GET" or not form.validate():
            form.source.choices = [
                (financial.source.name, financial.source.name),
            ]
            form.source.data = financial.source
            form.year.data = financial.year
            form.quarter.data = financial.quarter
            form.net_income.data = financial.net_income
            form.shares_outstanding.data = financial.shares_outstanding
            form.free_cash_flow.data = financial.free_cash_flow
            form.cash_flow_from_operating_activities.data = financial.cash_flow_from_operating_activities
            form.dividends_per_share.data = financial.dividends_per_share
            form.revenue.data = financial.revenue
            form.capex.data = financial.capex
            form.total_assets.data = financial.total_assets
            form.total_liabilities.data = financial.total_liabilities
            form.net_debt.data = financial.net_debt
            form.interest_coverage.data = financial.interest_coverage
            form.dividend_yield.data = financial.dividend_yield
            form.min_stock_price.data = financial.min_stock_price
            form.max_stock_price.data = financial.max_stock_price
            form.price_earnings_ratio_ltm.data = financial.price_earnings_ratio_ltm

            return self.render(
                "company_financial_edit_template.html",
                form=form,
                company=company,
                financial=financial,
                return_url="/admin/company/"
            )

        financial.source = form.source.data
        financial.year = form.year.data
        financial.quarter = form.quarter.data
        financial.net_income = form.net_income.data
        financial.shares_outstanding = form.shares_outstanding.data
        financial.free_cash_flow = form.free_cash_flow.data
        financial.cash_flow_from_operating_activities = form.cash_flow_from_operating_activities.data
        financial.dividends_per_share = form.dividends_per_share.data
        financial.revenue = form.revenue.data
        financial.capex = form.capex.data
        financial.total_assets = form.total_assets.data
        financial.total_liabilities = form.total_liabilities.data
        financial.net_debt = form.net_debt.data
        financial.interest_coverage = form.interest_coverage.data
        financial.dividend_yield = form.dividend_yield.data
        financial.min_stock_price = form.min_stock_price.data
        financial.max_stock_price = form.max_stock_price.data
        financial.price_earnings_ratio_ltm = form.price_earnings_ratio_ltm.data

        company_financial_repository.save(financial)

        if '_add_another' in request.form:
            return redirect(f"/admin/company/{company.id}/financial/create")
        elif '_continue_editing' in request.form:
            return redirect(f"/admin/company/{company.id}/financial/{financial.id}/edit")
        else:
            flash(gettext('Record was successfully saved.'), 'success')
            return redirect(f"/admin/company/{company.id}/financial")

    @expose('/<int:id>/financial/<int:financial_id>/delete', methods=["POST"])
    def financial_delete(self, id, financial_id):
        company_repository = CompanyRepository(sync=True)
        company: Company = company_repository.find_one(id=id)

        if company is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(f"/admin/company")

        company_financial_repository = FinancialRepository(sync=True)
        financial: Financial = company_financial_repository.find_one(id=financial_id, company_id=company.id)

        if financial is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(f"/admin/company/{company.id}/financial")

        company_financial_repository.delete(financial)

        count = 1
        flash(
            ngettext(
                'Record was successfully deleted.',
                '%(count)s records were successfully deleted.',
                count, count=count
            ),
            'success'
        )
        return redirect(f"/admin/company/{company.id}/financial")
