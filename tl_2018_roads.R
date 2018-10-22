library(sf)
library(dplyr)
library(data.table)
library(readr)
options(scipen = 999)

block_road_data <- function(state_code, block_dir, road_dir){
  
  #Reading shapefile directories and ordering them.
  block_layer_list <- st_layers(block_dir)
  block_order <- block_layer_list$name[order(block_layer_list$name)]
  
  road_layer_list <- st_layers(road_dir)
  road_order <- road_layer_list$name[order(road_layer_list$name)]
  
  n_counties <- length(block_order)
  
  state_df <- NULL
  
  for (j in 1:n_counties){
    cat("State:", state_code, "County:", j, "")
    
    #Reading and cleaning individual shapefiles.
    block <- st_read(block_dir, layer = block_order[j], quiet = TRUE)
    block <- block[ , c('GEOID10', 'UR10', 'UATYPE', 'ALAND10', 'AWATER10', 'geometry')]
    
    road <- st_read(road_dir, layer = road_order[j], quiet = TRUE)
    road <- road[ , c('geometry')]
    
    #Intersecting line and polygon, and finding lengths.
    ints <- st_intersection(block, road)
    ints$lengths <- st_length(ints)
    ints$GEOID10 <- factor(ints$GEOID10)
    ints$geometry <- NULL
    
    #Aggregating lengths.
    ints_table <- as.data.table(ints)
    road_lengths <- ints_table[ , (total_length = sum(lengths)), by = GEOID10]
    df <- as.data.frame(road_lengths)
    
    block$geometry <- NULL
    final <- merge(df, block, by = "GEOID10")
    state_df <- rbind(state_df, final)
  }
  
  csv_link <- paste0("./tl_2018_", state_code, "_road_lengths.csv")
  write.table(state_df, file = csv_link, sep = ",", row.names = FALSE, qmethod = "double")

  }

state_codes <- c('01', '04', '05', '06', '08', '09', '10', '12', '13', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26',
                 '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '44', '45', '46', '47',
                 '48', '49', '50', '51', '53', '54', '55', '56')
n_states <- length(state_codes)

for (i in 1:n_states){
  state <- state_codes[i]
  block_layers <- paste0("./Block/tl_2018_", state_codes[i], "_blocks")
  road_layers <- paste0("./Roads/tl_2018_", state_codes[i], "_roads")
  block_road_data(state, block_layers, road_layers)
}

init <- NULL
for (i in 1:n_states){
  csv_link <- paste0("./tl_2018_", state_codes[i], "_road_lengths.csv")
  data <- read_csv(csv_link, col_types = cols(GEOID10 = col_character(), V1 = col_double(), UR10 = col_character(), 
                                              UATYPE = col_character(), ALAND10 = col_double(), AWATER10 = col_double()))
  init <- bind_rows(init, data)
}

write.table(init, file = "./tl_2018_road_lengths.csv", sep = ",", row.names = FALSE, qmethod = "double")