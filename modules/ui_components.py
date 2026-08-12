import streamlit as st


def page_header(
    title,
    subtitle=None,
    icon="",
):
    if icon:
        st.title(
            f"{icon} {title}"
        )
    else:
        st.title(title)

    if subtitle:
        st.caption(subtitle)


def section_header(
    title,
    icon="",
):
    if icon:
        st.subheader(
            f"{icon} {title}"
        )
    else:
        st.subheader(title)


def success_box(
    message,
):
    st.success(message)


def info_box(
    message,
):
    st.info(message)


def warning_box(
    message,
):
    st.warning(message)


def metric_row(
    metrics,
):
    columns = st.columns(
        len(metrics)
    )

    for column, metric in zip(
        columns,
        metrics,
    ):
        with column:
            if isinstance(
                metric,
                dict,
            ):
                st.metric(
                    metric.get(
                        "label",
                        "",
                    ),
                    metric.get(
                        "value",
                        "",
                    ),
                    metric.get(
                        "delta",
                        None,
                    ),
                )
            else:
                st.metric(
                    str(metric),
                    "",
                )


def divider():
    st.divider()


def empty_state(
    message,
):
    st.info(message)


def error_box(
    message,
):
    st.error(message)


def metric_card(
    label,
    value,
):
    st.metric(
        label,
        value,
    )


def job_card(
    job,
):
    title = job.get(
        "title",
        job.get(
            "role",
            "Executive Position",
        ),
    )

    company = job.get(
        "company",
        "Company",
    )

    location = job.get(
        "location",
        "",
    )

    score = job.get(
        "executive_score",
        job.get(
            "score",
            0,
        ),
    )

    apply_link = job.get(
        "apply_link",
        "",
    )

    st.markdown(
        f"### {title}"
    )

    st.write(
        f"**Company:** {company}"
    )

    if location:
        st.write(
            f"**Location:** {location}"
        )

    st.metric(
        "Executive Fit",
        f"{score}%",
    )

    if apply_link:
        st.link_button(
            "🚀 Apply Now",
            apply_link,
            use_container_width=True,
        )

    st.divider()