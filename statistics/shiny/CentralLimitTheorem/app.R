#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)

# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Centralne Twierdzenie Graniczne"),

    # Sidebar with sliders 
    sidebarLayout(
        sidebarPanel(
            sliderInput("n_repetitions",
                        "Liczba losowań:",
                        min = 1,
                        max = 50000,
                        value = 5000),
            sliderInput("N_sample",
                        "Liczebność próby:",
                        min = 5,
                        max = 100,
                        value = 50),
            sliderInput("mu1",
                        "Średnia pierwszej populacji",
                        min = 0,
                        max = 200,
                        value = 0),
            sliderInput("mu2",
                        "Średnia drugiej populacji",
                        min = 0,
                        max = 200,
                        value = 20),
            sliderInput("sd1",
                        "Odchylenie standardowe pierwszej populacji:",
                        min = 1,
                        max = 30,
                        value = 15),
            sliderInput("sd2",
                        "Odchylenie standardowe drugiej populacji:",
                        min = 1,
                        max = 30,
                        value = 20),
            
        ),

        # Show the plot
        mainPanel(
           plotOutput("distPlot")
        )
    )
)

# Define server logic
server <- function(input, output) {

    output$distPlot <- renderPlot({
        
      # Liczebnosc probki
        N <- input$N_sample
        
      # Liczba powtorzen
        n <- input$n_repetitions
        
      # Srednia i SD dla populacji 1
        mu1 <- input$mu1
        mu2 <- input$mu2
        
      # Srednia i SD dla populacji 2
        sd1 <- input$sd1
        sd2 <- input$sd2
        
      # Wektor srednich z losowan dla populacji 1
        x <- replicate(
          n,
          mean(rnorm(N,mu1,sd1))
        )
        
      # Wektor srednich z losowan dla populacji 2
        y <- replicate(
          n,
          mean(rnorm(N,mu2,sd2))
        )

        color1 <- adjustcolor("#E86767",alpha.f = 0.4)
        color2 <- adjustcolor("#065FD3",alpha.f = 0.4)
        
        SD <- max(sd1,sd2)
        
        titl <- paste("n1 = ", N, ", m1 = ", mu1, " sd1 = ", sd1,
                      "\nn2 = ", N, " m2 = ", mu2, " sd2 = ", sd2)
        
        
        hist(x, col = color1, border = 'black',
             xlim = c(min(x,y)-SD,max(x,y)+SD),
             freq = F,
             xlab = "",
             main = titl)
        
        hist(y, col = color2, border = 'black',
             freq = F,
             add = TRUE)
        
        curve({dnorm(x,mean = mu1, sd = sd1)},
              col = "#E86767",
              lwd = 2,
              add = T)
        
        curve({dnorm(x,mu2,sd2)},
              col = "#065FD3",
              lwd = 2,
              add = T)
        
    })
}

# Run the application 
shinyApp(ui = ui, server = server)
