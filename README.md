# ternary_plotter

To run, just open the html file in a browser.

This program uses the following math to make sure the values sum to 1 and then to plot the ternary points on the chosen chart:

g = (a + b + c) / 1.0;

a = a * g;

b = b * g;

c = c * g;


x = (2.0 * c + a) / (a + b + c) / 2.0;

y = a / (a + b + c);

The x and y values are then scaled and translated to fit into the chart that is in the chosen image.
