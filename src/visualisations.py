import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import folium
from wordcloud import WordCloud
import cartopy

def plot_wordcloud(df = None,           # : pd.DataFrame,
                    axis = None,
                    tokenizer = None,   # : nltk.tokenize
                    stopwords = None    # : wordcloud.STOPWORDS
                    ):
    '''
    Plots wordcloud.
        Tokenizes text(s) and generates long string to plot cloud of words

        https://stackoverflow.com/questions/28786534/increase-resolution-with-word-cloud-and-remove-empty-border
    '''
    #stopwords = set(STOPWORDS)
    comment_words = ''
    for text in df:
        try:
            tokens = tokenizer.tokenize(text)
            comment_words += "".join(text) + " "
        except ValueError:
            None

    wordcloud = WordCloud(width=1200, height=800,
                          include_numbers=True, prefer_horizontal=0.95,
                          background_color ='white', # black
                          #stopwords = stopwords, # custom list of stopwords
                          max_words=350,
                          min_font_size=12, random_state=42).generate(comment_words)

    # plot the WordCloud image
    axis.imshow(wordcloud)
    axis.set_axis_off()
    #plt.tight_layout(pad = 0)

    return axis

def plot_folium_map_with_circles(df_to_plot = None, # : pd.DataFrame,
                                 map_object = None,
                                 save=False
                                 ):
    '''
        Docstring placeholder
    '''
    if map_object is None:
        map_object = folium.Map(
            width='80%', height='100%', left='10%',
            #tiles='CartoDB positron',
            location = [61.3508, 15.0973],
            zoom_start=5, min_zoom=2,
            min_lot=-20, max_lot=60, min_lat=40, max_lat=75,
            max_bounds=True,
            scrollWheelZoom=False, dragging=False
        )

    for indx, elem in df_to_plot.iterrows():
        color = mcolors.rgb2hex(plt.cm.Set1.colors[indx % len(plt.cm.Set1.colors)])

        folium.CircleMarker(
            location = [elem.lat, elem.lon],
            radius = elem.translated_text / df_to_plot.translated_text.max() * 30,
            fill=True, fill_color=color, color=color,
            popup="City: {}. Texts: {:,}".format(elem.city, int(elem.translated_text))
            ).add_to(map_object)

    #folium.LayerControl().add_to(m)
    # add reset to initial zoom and loc buttom if avaliable

    if save:
        map_object.save('../figures/Map_all_texts.html')

    return map_object

def plot_lines_yoy(df_to_plot,  # pd.DataFrame
                    axes,       # plt.ax
                    columns     # list[str]
                    ):
    '''
        Placeholder

        Need refactor to handle YOY, YTD, YOY growth in one function
    '''
    for indx, type_violence in enumerate(columns):
        df_aux = df_to_plot.groupby('Year')[type_violence]
        df_aux.plot.line(ax=axes[indx], style='--', marker='.')
        axes[indx].set_title(type_violence, loc='left')

        axes[indx].set_xticks(ticks=range(0, 12))
        axes[indx].set_xticklabels(labels=range(1, 12 + 1))

        if indx == 0:
            axes[indx].spines[["top", "right", "left"]].set_visible(False)
        elif (indx) % 2 == 0:
            axes[indx].yaxis.tick_right()
            axes[indx].spines[["top", "right"]].set_visible(False)
        else:
            axes[indx].spines[["top", "left"]].set_visible(False)

        axes[indx].grid(axis='y', alpha=0.4, linestyle='-', lw=0.5)
        #axes[indx].set_yticks([range(1, 12)])

        #break
    return axes

def _draw_pie_marker(xs, ys,
                    ratios, sizes,
                    colors, ax
                    ):
    '''
        Placeholder

        Source(s):
        * https://stackoverflow.com/questions/56337732/how-to-plot-scatter-pie-chart-using-matplotlib
        https://stackoverflow.com/questions/51409257/exploding-wedges-of-pie-chart-when-plotting-them-on-a-map-python-matplotlib
        https://www.geophysique.be/2010/11/26/matplotlib-basemap-tutorial-06-real-case-pie-charts/
        https://stackoverflow.com/questions/45266955/adding-pie-chart-at-given-coordinates-to-cartopy-projection
        https://stackoverflow.com/questions/24307549/place-pie-charts-on-a-map-using-basemap
    '''
    assert sum(ratios) <= 1, 'sum of ratios needs to be < 1'

    markers = []
    previous = 0
    # calculate the points of the pie pieces
    for color, ratio in zip(colors, ratios):
        this = 2 * np.pi * ratio + previous
        x  = [0] + np.cos(np.linspace(previous, this, 10)).tolist() + [0]
        y  = [0] + np.sin(np.linspace(previous, this, 10)).tolist() + [0]
        xy = np.column_stack([x, y])
        previous = this
        markers.append({'marker' : xy, 's' : np.abs(xy).max() ** 2 * np.array(sizes),
                        'facecolor' : color
                       })

    # scatter each of the pie pieces to create pies
    for marker in markers:
        ax.scatter(xs, ys, **marker)

    return ax

def _add_geo_basemap(extents=None,
                    projection=None,
                    ax=None
                    ):
    '''
        Placeholder
        https://rabernat.github.io/research_computing_2018/maps-with-cartopy.html
        https://stackoverflow.com/questions/67508054/improve-resolution-of-cartopy-map
        https://scitools.org.uk/cartopy/docs/v0.15/matplotlib/intro.html
        https://scitools.org.uk/cartopy/docs/latest/gallery/miscellanea/tube_stations.html
    '''
    ax.set_extent(extents, crs=projection)
    #axes.stock_img()
    #axes[indx].background_img(name='ETOPO', resolution='high')
    ax.add_feature(cartopy.feature.COASTLINE, zorder=90, lw=0.5)
    ax.add_feature(cartopy.feature.BORDERS, zorder=91)
    ax.add_feature(cartopy.feature.OCEAN)
    ax.add_feature(cartopy.feature.LAND, color='white', edgecolor='black')
    ax.add_feature(cartopy.feature.LAKES, edgecolor='black', lw=0.2)
    ax.add_feature(cartopy.feature.RIVERS)
    ax.gridlines(alpha=0.1, color='grey')
    return ax
