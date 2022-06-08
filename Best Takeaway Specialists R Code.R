theData = read.csv("C:/Users/David/Desktop/Rotman MMA Summer Datathon NWHL.csv")
subData = subset(theData, Event == "Takeaway")
playerByFrequency = data.frame(table(subData$Player))
sortedData = playerByFrequency[order(-playerByFrequency$Freq),]
topTenPlayers = sortedData[1:10,]
barplot(setNames(topTenPlayers$Freq, topTenPlayers$Var1), main = "Best Takeaway specialists", xlab = "Players", ylab = "Number of successful takeaways")
