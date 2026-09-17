import numpy as np
import matplotlib.pyplot as plt

mycolors = ["#785EF0", "#7DDEB2", "#DC267F", "#FE6100", "#FFB000", "#5F3331"]
translate_filters = {"u": 0, "g": 1, "r": 2, "i": 3, "z": 4, "y": 5}
translate_filternos = {v: k for (k, v) in translate_filters.items()}
    
# def plot_lc_dataframe(
#     df,
#     ax=None,
#     mjd_col="mjd",
#     flux_col="flux",  # TODO add support for mag
#     fluxerr_col="flux_err",  # TODO and magerr
#     flt_col="fltnum",
#     filter_map=translate_filternos,
#     color_map=mycolors,
#     show_labels=True,
#     **kwargs,
# ):
#     if len(df) != 1:
#         raise NotImplementedError(
#             "Currently only supports plotting one object at a time (one row in the DataFrame)."
#         )

#     row = df.rows(named=True)[0]

#     fmt = kwargs.pop("fmt", "-")
#     alpha = kwargs.pop("alpha", 0.7)
#     markersize = kwargs.pop("markersize", 5)
#     fill_alpha = kwargs.pop("fill_alpha", 0.1)
#     label_prefix = kwargs.pop("label_prefix", None)

#     if ax is None:
#         fig, ax = plt.subplots()

#     mjds = np.array(row[mjd_col])
#     fluxes = np.array(row[flux_col])
#     flts = np.array(row[flt_col])
#     fluxerrs = np.array(row[fluxerr_col]) if fluxerr_col in row else None

#     unique_filters = sorted(list(filter_map.keys()))

#     for it_num, f_idx in enumerate(unique_filters):
#         mask = flts == f_idx
#         sorted_idx = np.argsort(mjds[mask])

#         if show_labels:
#             label = filter_map[f_idx] if filter_map else f"Filter {f_idx}"
#             label = f"{label_prefix}{label}" if label_prefix is not None else label
#         else:
#             label = None

#         if color_map:
#             if isinstance(color_map, dict):
#                 color = color_map.get(f_idx, "black")
#             elif isinstance(color_map, list):
#                 color = color_map[it_num % len(color_map)]

#         t = mjds[mask][sorted_idx]
#         y = fluxes[mask][sorted_idx]

#         ax.errorbar(
#             x=t,
#             y=y,
#             fmt=fmt,
#             color=color,
#             label=label,
#             alpha=alpha,
#             markersize=markersize,
#             **kwargs,
#         )

#         if fluxerrs is not None:
#             yerr = fluxerrs[mask][sorted_idx]
#             ax.fill_between(
#                 x=t,
#                 y1=y - yerr,
#                 y2=y + yerr,
#                 color=color,
#                 alpha=fill_alpha,
#             )

#     ax.set_xlabel("MJD")
#     ax.set_ylabel("Flux")
#     return ax


def plot_lc_dataframe(
    df,
    ax=None,
    mjd_col="mjd",
    flux_col="flux",  # TODO add support for mag
    fluxerr_col="flux_err",  # TODO and magerr
    flt_col="fltnum",
    filter_map=translate_filternos,
    color_map=mycolors,
    show_labels=True,
    error_style="fill",  # NEW: Choose 'fill', 'bar', or 'both'
    **kwargs,
):
    if len(df) != 1:
        raise NotImplementedError(
            "Currently only supports plotting one object at a time (one row in the DataFrame)."
        )

    row = df.rows(named=True)[0]

    # Pop kwargs intended for specific matplotlib elements
    fmt = kwargs.pop("fmt", "-")
    alpha = kwargs.pop("alpha", 0.7)
    markersize = kwargs.pop("markersize", 5)
    fill_alpha = kwargs.pop("fill_alpha", 0.1)
    label_prefix = kwargs.pop("label_prefix", None)

    if ax is None:
        fig, ax = plt.subplots()

    mjds = np.array(row[mjd_col])
    fluxes = np.array(row[flux_col])
    flts = np.array(row[flt_col])
    fluxerrs = np.array(row[fluxerr_col]) if fluxerr_col in row else None

    unique_filters = sorted(list(filter_map.keys()))

    for it_num, f_idx in enumerate(unique_filters):
        mask = flts == f_idx
        sorted_idx = np.argsort(mjds[mask])

        if show_labels:
            label = filter_map[f_idx] if filter_map else f"Filter {f_idx}"
            label = f"{label_prefix}{label}" if label_prefix is not None else label
        else:
            label = None

        if color_map:
            if isinstance(color_map, dict):
                color = color_map.get(f_idx, "black")
            elif isinstance(color_map, list):
                color = color_map[it_num % len(color_map)]
        else:
            color = None

        t = mjds[mask][sorted_idx]
        y = fluxes[mask][sorted_idx]
        
        # Extract yerr BEFORE the errorbar call
        yerr = fluxerrs[mask][sorted_idx] if fluxerrs is not None else None

        # Determine if we should plot standard vertical bars
        bar_yerr = yerr if (error_style in ["bar", "both"] and yerr is not None) else None

        ax.errorbar(
            x=t,
            y=y,
            yerr=bar_yerr,  # Pass vertical errors here
            fmt=fmt,
            color=color,
            label=label,
            alpha=alpha,
            markersize=markersize,
            **kwargs,
        )

        # Determine if we should plot the shaded fill region
        if yerr is not None and error_style in ["fill", "both"]:
            ax.fill_between(
                x=t,
                y1=y - yerr,
                y2=y + yerr,
                color=color,
                alpha=fill_alpha,
            )

    ax.set_xlabel("MJD")
    ax.set_ylabel("Flux")
    return ax