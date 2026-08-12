import streamlit as st

from modules.ats_matcher import ATSMatcher
from modules.profile_manager import ProfileManager


st.set_page_config(
    page_title="ATS Matcher",
    page_icon="🎯",
    layout="wide",
)


st.title("🎯 ATS Resume Matcher")

st.caption(
    "Match your Executive Profile against a target job description."
)


profile_manager = ProfileManager()
profile = profile_manager.load_profile()


if not profile:

    st.error(
        "Executive Profile not found. "
        "Please complete Executive Profile first."
    )

    st.stop()


st.success(
    "✅ Executive Profile Loaded"
)


st.subheader("🎯 Target Position")


col1, col2 = st.columns(2)


with col1:

    role = st.text_input(
        "Target Executive Role",
        value=str(
            profile.get(
                "current_role",
                "Head of Sales",
            )
        ),
    )


with col2:

    company = st.text_input(
        "Company",
        value="Confidential",
    )


st.subheader("📄 Job Description")


job_description = st.text_area(
    "Paste the complete Job Description",
    height=300,
    placeholder=(
        "Paste the complete job description here..."
    ),
)


st.divider()


if st.button(
    "🎯 Calculate ATS Match",
    type="primary",
    use_container_width=True,
):

    if not job_description.strip():

        st.warning(
            "Please paste a Job Description first."
        )

        st.stop()


    job = {

        "role": role.strip(),

        "company": company.strip(),

        "description": job_description.strip(),

    }


    try:

        matcher = ATSMatcher()

        result = matcher.match(
            profile,
            job,
        )


        st.session_state[
            "ats_result"
        ] = result


    except Exception as error:

        st.error(
            "ATS matching failed."
        )

        st.exception(error)


if "ats_result" in st.session_state:

    result = st.session_state[
        "ats_result"
    ]


    st.divider()

    st.subheader(
        "📊 ATS Match Result"
    )


    score = result.get(
        "match_score",
        result.get(
            "ats_score",
            0,
        ),
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "ATS Match Score",
            f"{score}%",
        )


    matched = result.get(
        "matched_skills",
        [],
    )


    with col2:

        st.metric(
            "Matched Skills",
            len(matched)
            if isinstance(
                matched,
                list,
            )
            else 0,
        )


    missing = result.get(
        "missing_skills",
        [],
    )


    with col3:

        st.metric(
            "Missing Skills",
            len(missing)
            if isinstance(
                missing,
                list,
            )
            else 0,
        )


    st.divider()


    st.subheader(
        "✅ Matched Skills"
    )


    if matched:

        for skill in matched:

            st.success(
                str(skill)
            )

    else:

        st.info(
            "No matched skills identified."
        )


    st.subheader(
        "⚠️ Missing Skills"
    )


    if missing:

        for skill in missing:

            st.warning(
                str(skill)
            )

    else:

        st.success(
            "No significant missing skills identified."
        )


    recommended = result.get(
        "recommended_keywords",
        [],
    )


    if recommended:

        st.subheader(
            "🔑 Recommended ATS Keywords"
        )

        st.write(
            ", ".join(
                str(keyword)
                for keyword in recommended
            )
        )


    recommendations = result.get(
        "recommendations",
        [],
    )


    if recommendations:

        st.subheader(
            "💡 Recommendations"
        )

        for recommendation in recommendations:

            st.write(
                f"• {recommendation}"
            )


st.divider()


st.success(
    "✅ ATS Matcher Ready"
)