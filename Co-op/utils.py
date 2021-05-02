import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Optional, List, Union


class GraphMaker:
    """Helper class to make graphs using seaborn and matplotlib

    Attributes:
        style(str): The style for all the graphs
        x_label(str): x axis label for the graph
        y_label(str): y axis label for the graph
        title(str): The title for the graph
        x(str): The column name of a pandas dataframe to be plotted on the x axis
        y(str): The column name of a pandas dataframe to be plotted on the y axis
        data(pd.DataFrame): A pandas dataframe with the data to be graphed
    """

    def __init__(self, style: str = 'darkgrid', x_label: str = '', y_label: str = '', title: str = '',
                 x: str = None, y: str = None, data: pd.DataFrame = None):
        """Creates a graph maker object

        Add all labels and data for any type of that graph
        """
        self.style = style
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.x = x
        self.y = y
        self.data = data

    def boxplot(self, xlim: tuple = None, ylim: tuple = None, figsize: tuple = None, rotation: int = None, hue: str = None, show_points: bool = False) -> Optional[sns.boxplot]:
        """Creates a seaborn boxplot

        Args:
            xlim: The x limits of the graph 
            ylim: The y limits of the graph 
            figsize: The size of the graph
            rotation: The rotation angle of the x labels
            hue: The column name of the pandas dataframe on which to split the data on a hue
            show_points: True indicates that the points should be drawn ontop of the boxplot; false otherwise
        Returns: 
            A seaborn boxplot which can then be shown
        """
        # validate that the person has passed the correct parameters
        try:
            sns.set_style(self.style)

            # check if the size has changed
            if figsize != None:
                sns.set(rc={'figure.figsize': figsize})

            # draw the boxplot, if hue is None it will not appear
            ax = sns.boxplot(data=self.data, x=self.x, y=self.y, hue=hue)

            # check graph limits
            if xlim != None:
                ax.set(xlim=xlim)
            if ylim != None:
                ax.set(ylim=ylim)

            # check if the x label names are rotated
            if rotation != None:
                ax.set_xticklabels(ax.get_xticklabels(), rotation=rotation)

            # add points on top of the boxplot if specified
            if show_points:
                ax = sns.swarmplot(x=self.x, y=self.y,
                                   data=self.data, color=".25", hue=hue)

            # add title names to the graph
            ax.set_title(self.title)
            ax.set_xlabel(self.x_label)
            ax.set_ylabel(self.y_label)

            return ax

        except:
            # display a message and return none
            print(
                "Incorrect data entered, check that you have entered correct column names and data types")

    def barplot(self, figsize: tuple = None, orient: str = 'v', hue: str = None) -> Optional[sns.barplot]:
        """Creates a seaborn barplot

        Args:
            figsize: The size of the graph
            orient: The orientation of the barplot; either horizontal or vertical
            hue: The column name of the pandas dataframe on which to split the data on a hue
        Returns: 
            A seaborn barplot which can then be shown
        """
        # validate that the person has passed the correct parameters
        try:
            sns.set_style(self.style)

            # check if the size has changed
            if figsize != None:
                sns.set(rc={'figure.figsize': figsize})

            # plot the barplot on the correct axis
            if orient == 'v':
                ax = sns.barplot(data=self.data, x=self.x, y=self.y, hue=hue)
            # assume the person is attempting to flip the graph
            elif orient == 'h':
                ax = sns.barplot(data=self.data, x=self.y,
                                 y=self.x, hue=hue, orient='h')
                # flip the labels
                self.x_label, self.y_label = self.y_label, self.x_label
            else:
                raise Exception(
                    f'Value for orient must be either "v" or "h" but {orient} was passed')

            # add title names to the graph
            ax.set_title(self.title)
            ax.set_xlabel(self.x_label)
            ax.set_ylabel(self.y_label)
            print("Done")

            # return the labels to normal state if flipped
            if orient == 'h':
                self.x_label, self.y_label = self.y_label, self.x_label

            return ax

        except Exception as e:
            # display a message and return none
            if not e:
                print(
                    "Incorrect data entered, check that you have entered correct column names and data types")
            else:
                print(e)

    def pie(self, x: List = None, decimals: int = 1, pctdistance: int = 1.15, labels: List = None, figsize: tuple = None, title: str = None) -> plt.pie:
        """Creates a piechart using matplotlib

        Args:
            x: Can be passed in the constructor, this is the data in the form of a 1D array for the pie chart
            decimals: The number of decimals to be outputted by the graph
            pctdistance: A value indicating the distance from the centre for the values. A value of 1 means that the values are on the edge of the graph
            labels: Form of a 1D array, gives the labels for the piechart
            figsize: The size of the graph as a tuple or iterable
            title: The title of the graph
        Returns: 
            A seaborn piechart which can be displayed
        """
        try:
            # set the number of decimals on the piechart
            autopct = f'%.{decimals}f%%'
            # check if the person has passed an xval initially or in the piechart function
            if x.any() != None:
                x_vals = x
            elif self.x == None:
                raise Exception("No data passed for the piechart")
            else:
                x_vals = self.data[self.x]

            # set the figsize
            if figsize != None:
                plt.rcParams["figure.figsize"] = figsize

            # draw the piechart
            plt.pie(x=x_vals, autopct=autopct,
                              pctdistance=pctdistance)
            plt.axis('equal')

            plt.legend(labels=labels, loc='center left',
                       bbox_to_anchor=(1, 0.5))

            # add title names to the graph
            if title == None:
                plt.title(self.title, y=1.12)
            else:
               plt.title(title, y=1.12) 

            return plt

        except Exception as e:
            print(f"Error: {e}")
    
    def scatterplot(self, reg_line: bool = False, figsize: tuple = None, truncate: bool = False, xlim: tuple = None, ylim: tuple = None) -> Union[sns.scatterplot, sns.regplot]: 
        """Creates a scatterplot using matplotlib

        Args:
            reg_line: True indicates a regplot (inclues regression line with the points); false indicates a regular scatterplot
            figsize: The size of the graph as a tuple or iterable
            truncate: True stops the regline at the data points, false stops it at the graph limits
            xlim: The x limits of the graph 
            ylim: The y limits of the graph 
        Returns: 
            A seaborn regplot or scatterplot which can be displayed
        """
        try:
            sns.set_style(self.style)

            # check if the size has changed
            if figsize != None:
                sns.set(rc={'figure.figsize': figsize})

            # check for the type of graph and graph it
            if reg_line:
                ax = sns.regplot(data=self.data, x=self.x, y=self.y, truncate=truncate)
            else:
                print(self.x, self.y)
                ax = sns.scatterplot(data=self.data, x=self.x, y=self.y)
            
            # check graph limits
            if xlim != None:
                ax.set(xlim=xlim)
            if ylim != None:
                ax.set(ylim=ylim)

            # add title names to the graph
            ax.set_title(self.title)
            ax.set_xlabel(self.x_label)
            ax.set_ylabel(self.y_label)
            print("Done")
            return ax

        
        except Exception as e:
            print(f"Error: {e}")