import pandas as pd

data = [
    ["legit_store_101", 12500, 500, 230, 1460, 0.045, 120, "YES", "YES", "ON", "POSITIVE", "COD", "YES", 25.0],
    ["scamshop_trendy", 520, 9000, 12, 60, 0.002, 15, "NO", "NO", "OFF", "NULL", "PREPAY", "NO", 0.06],
    ["fashion.boutique", 9800, 1100, 180, 980, 0.037, 105, "YES", "YES", "ON", "POSITIVE", "COD", "YES", 8.9],
    ["insta_gift_hub", 300, 5200, 8, 45, 0.001, 10, "NO", "NO", "OFF", "NULL", "ADVPAY", "NO", 0.05],
    ["dealsLuxury", 15000, 400, 300, 1800, 0.055, 150, "YES", "YES", "ON", "POSITIVE", "COD", "YES", 37.5],
    ["quickmoney_flip", 450, 6000, 5, 30, 0.003, 25, "NO", "NO", "OFF", "NULL", "ADVPAY", "NO", 0.07],
    ["shoes_deluxe_store", 8700, 900, 220, 1250, 0.046, 140, "YES", "YES", "ON", "POSITIVE", "COD", "YES", 9.6],
    ["sarah_beauty_page", 320, 1500, 15, 75, 0.005, 50, "NO", "YES", "OFF", "NULL", "PREPAY", "NO", 0.21],
    ["gadgetmart_original", 25000, 700, 380, 2000, 0.052, 130, "YES", "YES", "ON", "POSITIVE", "COD", "YES", 35.7],
    ["luxurydealz_fake", 650, 8000, 7, 40, 0.002, 20, "NO", "NO", "OFF", "NULL", "ADVPAY", "NO", 0.08],
    [""]
]

columns = [
    "handle", "followers", "following", "posts", "account_life_days",
    "engagement_rate", "bio_length", "contact_info", "website",
    "comments_status", "comment_type", "method_payment", "customer_tags",
    "follower_following_ratio"
]

df = pd.DataFrame(data, columns=columns)
df.to_csv("data.csv", index=False)
print("Sample dataset 'data.csv' created successfully!")