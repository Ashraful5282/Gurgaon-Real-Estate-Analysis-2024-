import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('data of gurugram real Estate.csv')

#data cleaning
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
df = df.drop_duplicates() #remove duplicate

#numerical columns cleaning
df['price'] = df['price'].astype(str).str.replace(',', '').astype(float) #convert price to float
df['area'] = df['area'].astype(str).str.replace(',', '').astype(int) #convert area to int
df['rate_per_sqft'] = df['rate_per_sqft'].astype(str).str.replace(',', '').astype(int) #convert rate per sqft to int


#categorical columns cleaning
df['status'] = df['status'].str.strip().str.lower() #clean status column
df['rera_approval'] = df['rera_approval'].str.strip().str.lower().map({'approved by rera':True,'not approved by rera':False})
df['flat_type'] = df['flat_type'].str.strip().str.lower() #clean flat type column

print(df['company_name'].value_counts().head(20))

df = df.drop_duplicates() #remove duplicate rows
print(df)
print(df.info())


#Q1. Which is the costliest flat in the dataset?
costliest_flat = df.loc[df['price'].idxmax()] 
print(f"The costliest flat is a{costliest_flat['bhk_count']} BHK flat located in {costliest_flat['locality']} with a price of {costliest_flat['price']/10000000:.2f} Crores in {costliest_flat['society']}Society." )

#Q2.Which locality has the highest average price?
locality_avg_price = df.groupby('locality')['price'].mean().idxmax()
print(f"The locality with the highest average price is {locality_avg_price}.")
#print(df.groupby('locality')['price'].mean().sort_values(ascending=False).head(10))


#Q3. Which locality has the highest rate per square foot?
locality_avg_rate = df.groupby('locality')['rate_per_sqft'].mean().idxmax()
print(f"The locality with the highest rate per square foot is {locality_avg_rate}.")


#Q4 Do ready-to-move properties cost more than under-construction properties?
ready_to_move_avg_price = df[df['status'] == 'ready to move']['price'].mean()
under_construction_avg_price = df[df['status'] == 'under construction']['price'].mean()
if ready_to_move_avg_price > under_construction_avg_price:
    print(f"Ready-to-move properties cost more on average with an average price of {ready_to_move_avg_price/10000000:.2f} Crores compared to under-construction properties with an average price of {under_construction_avg_price/10000000:.2f} Crores.") 
else:
    print(f"Under-construction properties cost more on average with an average price of {under_construction_avg_price/10000000:.2f} Crores compared to ready-to-move properties with an average price of {ready_to_move_avg_price/10000000:.2f} Crores.")


#Q5. Do RERA-approved properties command a price premium?
rera_approved_avg_price = df[df['rera_approval'] == True]['price'].mean()
rera_not_approved_avg_price = df[df['rera_approval'] == False]['price'].mean()
if rera_approved_avg_price > rera_not_approved_avg_price:
    print(f"RERA-approved properties command a price premium with an average price of {rera_approved_avg_price/10000000:.2f} Crores compared to non-RERA-approved properties with an average price of {rera_not_approved_avg_price/10000000:.2f} Crores.")  
else:
    print(f"Non-RERA-approved properties command a price premium with an average price of {rera_not_approved_avg_price/10000000:.2f} Crores compared to RERA-approved properties with an average price of {rera_approved_avg_price/10000000:.2f} Crores.")


# #Q6. How does area (sqft) impact property price?
# sns = sns.scatterplot(data=df, x='area', y='price')
# plt.title('Area vs Price')
# # #plt.show()

#Q7. Which BHK configuration is the most expensive on per square foot basis?
bhk_avg_rate = df.groupby('bhk_count')['rate_per_sqft'].mean().idxmax()
print(f"The BHK configuration with the highest average rate per square foot is {bhk_avg_rate} BHK.")


#Q8. Which property type (Apartment, Floor, Plot) is the costliest?
most_expensive_property_type = df.groupby('flat_type')['rate_per_sqft'].mean().idxmax()
print(f"The costliest property type is {most_expensive_property_type}.")

#Q9. Do certain builders or companies consistently price higher?
print("The top 5 builders with the highest average rate per square foot are:")
top_5_builders = df.groupby('company_name')['rate_per_sqft'].mean().sort_values(ascending=False).head(5)
for builder, rate in top_5_builders.items():
    print(f"{builder}: {rate} per sqft")


# #Q10. Are larger homes always more expensive per square foot?
# sns.scatterplot(data=df, x='area', y='rate_per_sqft')
# plt.title('Area vs Rate per Square Foot')
# plt.show()