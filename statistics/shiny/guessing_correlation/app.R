#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(mvtnorm)
library(varhandle)
library(dplyr)


# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Zgadnij Korelację"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            sliderInput("margin",
                        "Możesz zmienić dopuszczalny margines błędu:",
                        min = 0,
                        max = 0.5,
                        value = 0.1),
            
            actionButton("generate",
                         "Generuj wykres!"),
            
            textInput("guess",
                      "Spróbuj zgadnąć korelację:",
                      placeholder = "0."),
            
            textOutput("feedback"),
            
            actionButton("check",
                         "Sprawdź"),
            textOutput("Result"),
            
            textOutput("points")
        ),

        # Show a plot of the generated distribution
        mainPanel(
           plotOutput("scatterplot")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  
  score <- 0
  
  observeEvent(input$generate,{
    
    output$Result <- renderText({""})
    
    output$scatterplot <- renderPlot({
      
      covar <- runif(1,0,3)
      sigma <- matrix(c(4,covar,covar,3), ncol=2)
      x <- rmvnorm(n=500, mean=c(1,2), sigma=sigma)
      
      correlation <<- round(cor(x)[2],2)
      
      
      plot(x)
      
    })
  })
  observeEvent(input$check, {
    
    guessNumb <- input$guess
    
    if(check.numeric(guessNumb)) {
      
      # Acceptable input:
      output$feedback <- renderText({""})
      
      guessNumb <- as.numeric(guessNumb)
      
      if(between(guessNumb,correlation-input$margin,correlation+input$margin)){
        
        # Good answer:
        
        output$Result <- renderText({
          
          paste("Brawo! Prawdziwa korelacja: ",
                correlation,
                ", Twoja odpowiedź: ",
                guessNumb)
          
        })
        
        score <<- score + 1

        # Wrong answer:
        
      } else {
        
        output$Result <- renderText({
          paste("Buuu! Prawdziwa korelacja: ",
                correlation,
                ", Twoja odpowiedź: ",
                guessNumb)
        })
      }
      
      # Wrong input:
    } else {
      output$feedback <- renderText({
        "Twoja odpowiedź powinna być ułamkiem dziesiętnym między 0 a 1"
      })
    }
    
    output$points <- renderText({
      paste("Masz obecnie ", score, " punktów.")
    })
    
  })
  


}

# Run the application 
shinyApp(ui = ui, server = server)
