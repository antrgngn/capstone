library(Synth)
library(dplyr)
library(ggplot2)


fashion_data <- read.csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTxFyXB-ZRqHMEcmVmNSZXmzzskqJjHVMfP-aC6LhPB_Z7ssW7oG20gNZedec4-_hQLovgJEiMjZ_r6/pub?gid=606552048&single=true&output=csv")

# Create a numeric ID for each fashion house
house_ids <- data.frame(
  house = unique(fashion_data$house),
  house_id = 1:length(unique(fashion_data$house))
)

# Join the IDs to the main dataset
fashion_data <- fashion_data %>%
  left_join(house_ids, by = "house")

# Add a time variable (convert year+season to a numeric time point)
fashion_data <- fashion_data %>%
  mutate(time = as.numeric(year) + ifelse(season == "ss", 0, 0.5))

# Define treatment parameters
treatment_house <- "Louis Vuitton"
treatment_id <- house_ids$house_id[house_ids$house == treatment_house]
treatment_time <- 2023  # Pharrell Williams joined in 2023
control_ids <- house_ids$house_id[house_ids$house != treatment_house]

# Data preparation for Synth with your column names
dataprep.out <- dataprep(
  foo = fashion_data,
  predictors = c( 
    "london", 
    "milan", 
    "director_years"
  ),
  predictors.op = "mean",  # Operation to perform on predictors
  
  # Special predictors - sentiment lags (adjusted for 2018-2023 pre-treatment period)
  special.predictors = list(
    list("fashion_magazine_sentiment", seq(2018, 2019, by = 0.5), "mean"),
    list("fashion_magazine_sentiment", seq(2019.5, 2021, by = 0.5), "mean"),
    list("fashion_magazine_sentiment", seq(2021.5, 2022.5, by = 0.5), "mean")
  ),
  
  dependent = "fashion_magazine_sentiment",
  unit.variable = "house_id",
  time.variable = "time",
  treatment.identifier = treatment_id,
  controls.identifier = control_ids,
  time.predictors.prior = seq(2018, 2022.5, by = 0.5),  # Pre-treatment period
  time.optimize.ssr = seq(2018, 2022.5, by = 0.5),      # Pre-treatment period
  unit.names.variable = "house",
  time.plot = seq(2018, 2024.5, by = 0.5)               # Full time period through 2024
)

# Run the synthetic control
synth.out <- synth(dataprep.out)





# Path plot (comparing actual vs synthetic)
path.plot(
  synth.res = synth.out,
  dataprep.res = dataprep.out,
  tr.intake = treatment_time,
  Ylab = "Fashion Magazine Sentiment",
  Xlab = "Year",
  Legend = c("Louis Vuitton", "Synthetic Louis Vuitton"),
  Main = "Impact of Pharrell Williams as Creative Director at Louis Vuitton"
)
abline(v = treatment_time, lty = "dashed")




