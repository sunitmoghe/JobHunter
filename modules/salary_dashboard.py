import streamlit as st

def render_salary_dashboard(
    jobs,
    salary_engine,
    experience,
):

    # --------------------------------------------------
    # SALARY INTELLIGENCE
    # --------------------------------------------------

    if jobs:

        st.header("💰 Executive Salary Intelligence")

        selected_job = st.selectbox(

            "Select Job",

            range(len(jobs)),

            format_func=lambda x:

            f"{jobs[x].get('role','')} - {jobs[x].get('company','')}"

        )

        selected = jobs[selected_job]

        role = selected.get(

            "role",

            selected.get(

                "title",

                ""

            )

        )

        country = selected.get(

            "country",

            "Singapore"

        )

        salary = salary_engine.get_salary_benchmark(

            country,

            role

        )

        if "average" in salary:

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(

                    "Low",

                    f"{salary['currency']} {salary['low']:,}"

                )

            with col2:

                st.metric(

                    "Average",

                    f"{salary['currency']} {salary['average']:,}"

                )

            with col3:

                st.metric(

                    "High",

                    f"{salary['currency']} {salary['high']:,}"

                )

        else:

            st.warning(

                salary.get(

                    "message",

                    "Salary benchmark unavailable."

                )

            )

    # --------------------------------------------------
    # OFFER COMPARISON
    # --------------------------------------------------

        st.subheader("📈 Compare Your Offer")

        offered_salary = st.number_input(

            "Enter Offered Salary",

            min_value=0,

            step=1000

        )

        if offered_salary > 0:

            comparison = salary_engine.compare_offer(

                country,

                role,

                offered_salary

            )

            if "rating" in comparison:

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(

                        "Market Average",

                        f"{salary['currency']} {comparison['market_average']:,}"

                    )

                with col2:

                    st.metric(

                        "Difference",

                        f"{comparison['difference_percentage']}%"

                    )

                if comparison["rating"] == "Excellent Offer":

                    st.success(

                        "🎉 Excellent Offer"

                    )

                elif comparison["rating"] == "Good Offer":

                    st.info(

                        "👍 Good Market Offer"

                    )

                else:

                    st.warning(

                        "⚠ Below Market Average"

                    )

    # --------------------------------------------------
    # EXECUTIVE MARKET POSITION
    # --------------------------------------------------

        st.subheader("🎯 Executive Market Position")

        recommendation = salary_engine.recommend_market_position(

            experience,

            "Executive"

        )

        st.success(

            recommendation["level"]

        )

        st.write(

            "### Recommended Roles"

        )

        for item in recommendation[

            "recommended_roles"

        ]:

            st.write(

                "•",

                item

            )

    # --------------------------------------------------
    # MARKET INSIGHTS
    # --------------------------------------------------

        st.subheader("🌍 AI Market Intelligence")

        if country == "Singapore":

            st.success(

                "Singapore remains one of the strongest executive hiring markets for technology, SaaS, Industrial Automation and Manufacturing."

            )

        elif country == "Germany":

            st.info(

                "Germany continues strong hiring across Industry 4.0, Manufacturing and Automation."

            )

        elif country == "UAE":

            st.success(

                "UAE has strong demand for enterprise sales leaders across Technology, Energy and Infrastructure."

            )

        elif country == "India":

            st.info(

                "India continues expanding executive hiring across SaaS, AI, Manufacturing and Telecom."

            )

        else:

            st.info(

                "Market intelligence is continuously improving."

            )

        st.divider()
