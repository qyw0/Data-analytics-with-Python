library(shiny)

function(input, output, session) {
  
  # Combine the selected variables into a new data frame

  Data1 <- reactive({
    file1 <- input$file1
    if (is.null(file1)){return(NULL)}
      
    df <- read.csv(file1$datapath, header = TRUE)
    if (is.null(df)) {return(NULL)}
    updateSelectInput(session, 'xcol', 'X Variable', names(df))
    updateSelectInput(session, 'ycol', 'Y Variable', names(df))
    df
  })
 
   
  output$plot1 <- renderPlot({

    data2 <- Data1()[, c(input$xcol, input$ycol)]
    if (is.null(data2)) {return(NULL)}
    x <- data2[[1]]
    y <- data2[[2]]
    
    if(input$D){
      if(is.vector(x) == "TRUE"){
        hist(x, main = 'Distribution of X variable')
      }else{
        barplot(summary(x))
      }
      
      
    }else{
      plot(data2)
    }
    
    
    if(input$L){
      abline(lm(y~x), col = 'red', lwd = input$Thickness/10)
    }

  })
  
}


