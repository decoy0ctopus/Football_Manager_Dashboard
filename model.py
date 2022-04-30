# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 10:33:03 2021

@author: patrick robinson

"""
# Must run init prior to running this script to get the dataset

#Import modules

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Polynomial Regression using camera footage to model goals from open play

X = dataset.iloc[:, 8:9].values
Y = dataset.iloc[:, 15].values

#Training the Polynomical Regression model on the whole dataset

poly_reg = PolynomialFeatures(degree = 4)
X_poly = poly_reg.fit_transform(X)
lin_reg_2 = LinearRegression()
lin_reg_2.fit(X_poly, Y)

#Visualising the Polynomial Regression results (for higher resolution and smoother curve)

# Creates a variable x_grid with smaller step value than x

X_grid = np.arange(min(X), max(X), 0.01)
X_grid = X_grid.reshape((len(X_grid), 1))

#replot the graph with x_grid instead of x

plt.scatter(X, Y, color = 'red')
plt.plot(X_grid, lin_reg_2.predict(poly_reg.fit_transform(X_grid)), color = 'blue')
plt.title('Camera Footage v Open Play Goals (Polynomial Regression)')
plt.xlabel('Camera Footage')
plt.ylabel('Goals from Open Play')
plt.show()

# Polynomial Regression using scouting footage to model open play goals

X = dataset.iloc[:, 9:10].values
Y = dataset.iloc[:, 15].values

#Training the Polynomical Regression model on the whole dataset

poly_reg = PolynomialFeatures(degree = 4)
X_poly = poly_reg.fit_transform(X)
lin_reg_2 = LinearRegression()
lin_reg_2.fit(X_poly, Y)

#Visualising the Polynomial Regression results (for higher resolution and smoother curve)

# Creates a variable x_grid with smaller step value than x

X_grid = np.arange(min(X), max(X), 0.01)
X_grid = X_grid.reshape((len(X_grid), 1))

#replot the graph with x_grid instead of x

plt.scatter(X, Y, color = 'red')
plt.plot(X_grid, lin_reg_2.predict(poly_reg.fit_transform(X_grid)), color = 'blue')
plt.title('Scouting v Open Play Goals (Polynomial Regression)')
plt.xlabel('Camera Footage')
plt.ylabel('Goals from Open Play')
plt.show()


# Polynomial Regression using camera footage to model set play goals

X = dataset.iloc[:, 8:9].values
Y = dataset.iloc[:, 14].values

# Training the Linear Regression model on the whole dataset

lin_reg = LinearRegression()
lin_reg.fit(X, Y)

#Training the Polynomical Regression model on the whole dataset

poly_reg = PolynomialFeatures(degree = 4)
X_poly = poly_reg.fit_transform(X)
lin_reg_2 = LinearRegression()
lin_reg_2.fit(X_poly, Y)

#Visualising the Polynomial Regression results (for higher resolution and smoother curve)

# Creates a variable x_grid with smaller step value than x

X_grid = np.arange(min(X), max(X), 0.01)
X_grid = X_grid.reshape((len(X_grid), 1))

#replot the graph with x_grid instead of x

plt.scatter(X, Y, color = 'red')
plt.plot(X_grid, lin_reg_2.predict(poly_reg.fit_transform(X_grid)), color = 'blue')
plt.title('Camera Footage v Set Play Goals (Polynomial Regression)')
plt.xlabel('Camera Footage')
plt.ylabel('Goals from Set Play')
plt.show()

# Polynomial Regression using scouting footage to model open play goals

X = dataset.iloc[:, 9:10].values
Y = dataset.iloc[:, 14].values

#Training the Polynomical Regression model on the whole dataset

poly_reg = PolynomialFeatures(degree = 4)
X_poly = poly_reg.fit_transform(X)
lin_reg_2 = LinearRegression()
lin_reg_2.fit(X_poly, Y)

#Visualising the Polynomial Regression results (for higher resolution and smoother curve)

# Creates a variable x_grid with smaller step value than x

X_grid = np.arange(min(X), max(X), 0.01)
X_grid = X_grid.reshape((len(X_grid), 1))

#replot the graph with x_grid instead of x

plt.scatter(X, Y, color = 'red')
plt.plot(X_grid, lin_reg_2.predict(poly_reg.fit_transform(X_grid)), color = 'blue')
plt.title('Scouting v Set Play Goals (Polynomial Regression)')
plt.xlabel('Camera Footage')
plt.ylabel('Goals from Set Play')
plt.show()

# Use Seaborn heatmap to produce a heatmap of data correlations within our dataset

ax = sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 120, n=200),
    square=True
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
);

pickle.dump(lin_reg_2, open('model.pkl','wb'))

model = pickle.load(open('model.pkl','rb'))
print(model.predict([4]))
