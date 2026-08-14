import streamlit as st

from modules.global_job_discovery_engine import (
    GlobalJobDiscoveryEngine,
)
from modules.global_job_enrichment_engine import (
    GlobalJobEnrichmentEngine,
)


st.set_page_config(
    page_title="Company & Job Intelligence",
    page_icon="🏢",
    layout="wide",
)


st.title("🏢 Company & Job Intelligence")

st.caption(
    "Enrich selected global executive opportunities with company, salary, application and public contact intelligence."
)


discovery = GlobalJobDiscoveryEngine()
enrichment = GlobalJobEnrichmentEngine()


# ==========================================================
# SEARCH
# ==========================================================

st.subheader("🔎 Find Executive Opportunities")

col1, col2 = st.columns(2)

with col1:

    role = st.text_input(
        "Executive Role",
        value="Head of Sales",
    )

with col2:

    country = st.selectbox(
        "Country",
        list(
            discovery.COUNTRIES.keys()
        ),
    )


search = st.button(
    "🔎 Search Opportunities",
    type="primary",
    use_container_width=True,
)


if search:

    with st.spinner(
        "Searching opportunities..."
    ):

        try:

            jobs = discovery.search(
                role=role.strip(),
                countries=[country],
                pages=2,
                results_per_page=20,
            )

            jobs = enrichment.enrich_jobs(
                jobs
            )

            st.session_state[
                "company_intelligence_jobs"
            ] = jobs

        except Exception as error:

            st.error(
                "Unable to search opportunities."
            )

            st.exception(
                error
            )


jobs = st.session_state.get(
    "company_intelligence_jobs",
    [],
)


# ==========================================================
# RESULTS
# ==========================================================

if jobs:

    st.divider()

    st.subheader(
        f"📊 Enriched Opportunities: {len(jobs)}"
    )


    # ------------------------------------------------------
    # QUICK SUMMARY
    # ------------------------------------------------------

    verified_websites = sum(
        1
        for job in jobs
        if job.get(
            "company_website_verified",
            False,
        )
    )

    salary_available = sum(
        1
        for job in jobs
        if job.get(
            "salary_available",
            False,
        )
    )

    recruiter_available = sum(
        1
        for job in jobs
        if job.get(
            "recruiter_contact_available",
            False,
        )
    )


    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Jobs",
            len(jobs),
        )

    with c2:

        st.metric(
            "Verified Websites",
            verified_websites,
        )

    with c3:

        st.metric(
            "Salary Available",
            salary_available,
        )

    with c4:

        st.metric(
            "Recruiter / HR Contact",
            recruiter_available,
        )


    st.divider()


    # ------------------------------------------------------
    # COMPANY FILTER
    # ------------------------------------------------------

    company_names = sorted(
        {
            str(
                job.get(
                    "company",
                    "",
                )
            ).strip()
            for job in jobs
            if job.get(
                "company"
            )
        }
    )


    selected_company = st.selectbox(
        "Company",
        ["All Companies"]
        + company_names,
    )


    filtered_jobs = jobs


    if selected_company != "All Companies":

        filtered_jobs = [
            job
            for job in jobs
            if job.get(
                "company"
            ) == selected_company
        ]


    # ------------------------------------------------------
    # JOB CARDS
    # ------------------------------------------------------

    for index, job in enumerate(
        filtered_jobs,
        start=1,
    ):

        role_name = job.get(
            "role",
            "Executive Position",
        )

        company_name = job.get(
            "company",
            "Unknown Company",
        )

        country_name = job.get(
            "country",
            "",
        )

        location = job.get(
            "location",
            "Not available",
        )

        salary = job.get(
            "salary",
            "Not disclosed",
        )

        currency = job.get(
            "currency",
            "",
        )

        source = job.get(
            "source",
            "Unknown",
        )

        age_hours = job.get(
            "age_hours"
        )

        freshness = job.get(
            "freshness_bucket",
            "UNKNOWN",
        )

        freshness_label = job.get(
            "freshness_label",
            "Posting age unavailable",
        )

        company_website = job.get(
            "company_website",
            "Not verified",
        )

        careers_page = job.get(
            "careers_page",
            "Not available",
        )

        contact_page = job.get(
            "contact_page",
            "Not available",
        )

        linkedin_company = job.get(
            "linkedin_company",
            "Not available",
        )

        recruiter_name = job.get(
            "recruiter_name",
            "Not available",
        )

        recruiter_email = job.get(
            "recruiter_email",
            "Not available",
        )

        recruiter_phone = job.get(
            "recruiter_phone",
            "Not available",
        )

        recruiter_linkedin = job.get(
            "recruiter_linkedin",
            "Not available",
        )

        completeness = job.get(
            "data_completeness",
            0,
        )

        verification = job.get(
            "website_verification",
            "Unavailable",
        )

        apply_link = job.get(
            "apply_link",
            "Not available",
        )


        if freshness == "IMMEDIATE":

            badge = "🚨"

        elif freshness == "VERY HIGH":

            badge = "🔥"

        elif freshness == "HIGH":

            badge = "🟠"

        elif freshness == "PRIORITY":

            badge = "🟡"

        else:

            badge = "🔵"


        with st.container(
            border=True
        ):

            title_col, urgency_col = st.columns(
                [5, 2]
            )


            with title_col:

                st.markdown(
                    f"### {index}. {role_name}"
                )

                st.write(
                    f"**{company_name}**"
                )

                st.caption(
                    f"📍 {location} | {country_name}"
                )


            with urgency_col:

                st.markdown(
                    f"### {badge} {freshness}"
                )

                st.caption(
                    freshness_label
                )


            # --------------------------------------------------
            # KEY METRICS
            # --------------------------------------------------

            metric1, metric2, metric3, metric4 = st.columns(4)

            with metric1:

                if age_hours is None:

                    st.metric(
                        "Posted Age",
                        "Unknown",
                    )

                elif job.get(
                    "future_timestamp",
                    False,
                ):

                    st.metric(
                        "Posted Age",
                        "Just posted",
                    )

                else:

                    st.metric(
                        "Posted Age",
                        f"{age_hours:.1f} hrs",
                    )


            with metric2:

                st.metric(
                    "Salary",
                    (
                        f"{currency} {salary}"
                        if currency
                        and salary
                        != "Not disclosed"
                        and salary
                        != "Not Disclosed"
                        else str(
                            salary
                        )
                    ),
                )


            with metric3:

                st.metric(
                    "Data Completeness",
                    f"{float(completeness):.0f}%",
                )


            with metric4:

                st.metric(
                    "Source",
                    source,
                )


            st.divider()


            # --------------------------------------------------
            # COMPANY INTELLIGENCE
            # --------------------------------------------------

            st.markdown(
                "#### 🏢 Company Intelligence"
            )

            company_col1, company_col2 = st.columns(
                2
            )


            with company_col1:

                st.write(
                    f"**Company:** {company_name}"
                )

                st.write(
                    f"**Industry:** "
                    f"{job.get('industry', 'Not available')}"
                )

                st.write(
                    f"**Employees:** "
                    f"{job.get('employee_count', 'Not available')}"
                )

                st.write(
                    f"**Headquarters:** "
                    f"{job.get('headquarters', 'Not available')}"
                )


            with company_col2:

                if (
                    company_website
                    != "Not verified"
                ):

                    st.link_button(
                        "🌐 Company Website",
                        company_website,
                    )

                    st.caption(
                        "Website status: Verified"
                    )

                else:

                    st.warning(
                        "Company website not verified."
                    )

                if careers_page != "Not available":

                    st.link_button(
                        "💼 Careers Page",
                        careers_page,
                    )

                if contact_page != "Not available":

                    st.link_button(
                        "📞 Contact Page",
                        contact_page,
                    )

                if linkedin_company != "Not available":

                    st.link_button(
                        "🔗 Company LinkedIn Search",
                        linkedin_company,
                    )


            # --------------------------------------------------
            # SALARY
            # --------------------------------------------------

            st.markdown(
                "#### 💰 Compensation"
            )

            salary_col1, salary_col2, salary_col3 = st.columns(
                3
            )


            with salary_col1:

                st.write(
                    f"**Posted Salary:** {salary}"
                )


            with salary_col2:

                st.write(
                    f"**Currency:** {currency}"
                )


            with salary_col3:

                if job.get(
                    "salary_available",
                    False,
                ):

                    st.success(
                        "✅ Salary from job posting"
                    )

                else:

                    st.info(
                        "Salary not disclosed"
                    )


            # --------------------------------------------------
            # RECRUITER / HR
            # --------------------------------------------------

            st.markdown(
                "#### 👤 Recruiter / HR Intelligence"
            )

            recruiter_col1, recruiter_col2 = st.columns(
                2
            )


            with recruiter_col1:

                st.write(
                    f"**Name:** {recruiter_name}"
                )

                st.write(
                    f"**Email:** {recruiter_email}"
                )

                st.write(
                    f"**Phone:** {recruiter_phone}"
                )


            with recruiter_col2:

                st.write(
                    f"**LinkedIn:** {recruiter_linkedin}"
                )

                if job.get(
                    "recruiter_contact_available",
                    False,
                ):

                    st.success(
                        "✅ Public recruiter/HR contact available"
                    )

                else:

                    st.info(
                        "Recruiter/HR contact not available in the source data."
                    )


            # --------------------------------------------------
            # APPLICATION
            # --------------------------------------------------

            st.markdown(
                "#### 🚀 Application"
            )


            if (
                apply_link
                and apply_link
                != "Not available"
            ):

                st.link_button(
                    "🚀 Open Job / Apply",
                    apply_link,
                    use_container_width=True,
                )

            else:

                st.warning(
                    "Application URL unavailable."
                )


            # --------------------------------------------------
            # VERIFICATION
            # --------------------------------------------------

            with st.expander(
                "🔎 Verification & Data Quality"
            ):

                st.write(
                    f"**Website verification:** {verification}"
                )

                flags = job.get(
                    "verification_flags",
                    [],
                )

                if flags:

                    st.write(
                        "**Data gaps:**"
                    )

                    for flag in flags:

                        st.write(
                            f"• {flag}"
                        )

                else:

                    st.success(
                        "No known data gaps."
                    )

else:

    st.info(
        "Search for an executive role to load company and job intelligence."
    )