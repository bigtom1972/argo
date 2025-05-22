
import matplotlib.pyplot as plt

# Sample data
x_values = list(range(1, 101))
y_rand_values = []
y_mix_values = []
with open('rand_100.log', 'r') as file:
    # Read all lines from the file
    lines = file.readlines()
for line in lines:
    y_rand_values.append(int(line.strip()))

with open('red_mix_blue_dist_100.log', 'r') as file:
    # Read all lines from the file
    lines = file.readlines()
for line in lines:
    y_mix_values.append(int(line.strip()))


y_average_rand = [sum(y_rand_values) / len(y_rand_values)] * 100
y_average_mix = [sum(y_mix_values) / len(y_mix_values)] * 100



# Create a figure and axis
fig, ax = plt.subplots()

# Plot the first line
ax.plot(x_values, y_rand_values, label='Random Values', color='blue')

# Plot the second line
ax.plot(x_values, y_mix_values, label='Mixed Values')

ax.plot(x_values, y_average_mix, label='average Mixed Values')
ax.plot(x_values, y_average_rand, label='average Random Values')
# Add a legend
ax.legend()

# Show the plot
plt.show()