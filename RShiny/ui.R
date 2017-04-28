library(shiny)

pageWithSidebar(
  headerPanel('Group9 Assignment5'),
  sidebarPanel(
    fileInput("file1", label = h3("File input")),
    
    checkboxInput("D", label = strong("Distribution"), value = FALSE),
    selectInput('xcol', 'X Variable', names(df), selected=names(df)[[1]]),
    selectInput('ycol', 'Y Variable', names(df), selected=names(df)[[2]]),
    checkboxInput("L", label = strong("Linear model"), value = FALSE),
    
    
    sliderInput("Thickness",
                "Line Thickness:",
                min = 1,  max = 100, value = 10)
    
    ),
  mainPanel(
    plotOutput('plot1')
  )
)
