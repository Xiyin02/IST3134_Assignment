#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <chrono>
#include <iomanip>

void printProgressBar(float progress, double timeElapsed) {
    int barWidth = 50;
    int pos = barWidth * progress;

    std::cout << "[";
    for (int i = 0; i < barWidth; ++i) {
        if (i < pos) std::cout << "=";
        else if (i == pos) std::cout << ">";
        else std::cout << " ";
    }
    std::cout << "] " << std::setw(3) << int(progress * 100.0) << "%  ";
    std::cout << "Time Spent: " << std::fixed << std::setprecision(2) << timeElapsed << " seconds\r";
    std::cout.flush();
}

void readInputFile(const std::string& filename, std::unordered_map<std::string, std::vector<std::pair<std::string, std::string> > >& userRatings) {
    std::ifstream inputFile(filename);
    if (!inputFile.is_open()) {
        std::cerr << "Error opening input file: " << filename << std::endl;
        return;
    }

    std::string line;
    int totalLines = 0;
    while (std::getline(inputFile, line)) {
        totalLines++;
    }

    inputFile.clear();
    inputFile.seekg(0, std::ios::beg);

    int currentLine = 0;
    auto startTime = std::chrono::high_resolution_clock::now();
    while (std::getline(inputFile, line)) {
        currentLine++;
        std::istringstream iss(line);
        std::string movie_id, user_id, rating, date;
        std::getline(iss, movie_id, ',');
        std::getline(iss, user_id, ',');
        std::getline(iss, rating, ',');
        std::getline(iss, date, ',');

        userRatings[user_id].push_back(std::make_pair(movie_id, rating));

        float progress = static_cast<float>(currentLine) / static_cast<float>(totalLines);
        auto endTime = std::chrono::high_resolution_clock::now();
        double timeElapsed = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime).count() / 1000.0;
        printProgressBar(progress, timeElapsed);
    }
    std::cout << std::endl;

    inputFile.close();
}

void writeOutputFile(const std::string& filename, const std::unordered_map<std::string, std::vector<std::pair<std::string, std::string> > >& userRatings) {
    std::ofstream outputFile(filename);
    if (!outputFile.is_open()) {
        std::cerr << "Error opening output file: " << filename << std::endl;
        return;
    }

    for (const auto& entry : userRatings) {
        const std::string& user_id = entry.first;
        const std::vector<std::pair<std::string, std::string> >& ratings = entry.second;
        std::vector<std::pair<std::string, std::string> > sortedRatings = ratings;
        std::sort(sortedRatings.begin(), sortedRatings.end());

        outputFile << user_id << "\t[";
        for (size_t i = 0; i < sortedRatings.size(); ++i) {
            if (i > 0) {
                outputFile << ",";
            }
            outputFile << "[" << sortedRatings[i].first << "," << sortedRatings[i].second << "]";
        }
        outputFile << "]" << std::endl;
    }

    outputFile.close();
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <inputFilename> <outputFilename>" << std::endl;
        return 1;
    }

    std::string inputFilename = argv[1];
    std::string outputFilename = argv[2];

    std::unordered_map<std::string, std::vector<std::pair<std::string, std::string> > > userRatings;
    readInputFile(inputFilename, userRatings);

    writeOutputFile(outputFilename, userRatings);

    return 0;
}
