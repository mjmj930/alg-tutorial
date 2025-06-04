#include <iostream>
#include <string>
#include <sstream>
#include <vector>

using namespace std;

const long long SECOND = 1;
const long long MINUTE = 60 * SECOND;
const long long HOUR = 60 * MINUTE;
const long long DAY = 24 * HOUR;
const long long MONTH = 31 * DAY;
const long long YEAR = 22 * MONTH;

long long unitToSeconds(const string& unit) {
    if (unit == "second" || unit == "seconds") return SECOND;
    if (unit == "minute" || unit == "minutes") return MINUTE;
    if (unit == "hour" || unit == "hours") return HOUR;
    if (unit == "day" || unit == "days") return DAY;
    if (unit == "month" || unit == "months") return MONTH;
    if (unit == "year" || unit == "years") return YEAR;
    return -1;
}

string formatDuration(long long totalSeconds) {
    vector<string> parts;

    long long years = totalSeconds / YEAR;
    totalSeconds %= YEAR;
    if (years > 0) parts.push_back(to_string(years) + " year");

    long long months = totalSeconds / MONTH;
    totalSeconds %= MONTH;
    if (months > 0) parts.push_back(to_string(months) + " month");

    long long days = totalSeconds / DAY;
    totalSeconds %= DAY;
    if (days > 0) parts.push_back(to_string(days) + " day");

    long long hours = totalSeconds / HOUR;
    totalSeconds %= HOUR;
    if (hours > 0) parts.push_back(to_string(hours) + " hour");

    long long minutes = totalSeconds / MINUTE;
    totalSeconds %= MINUTE;
    if (minutes > 0) parts.push_back(to_string(minutes) + " minute");

    long long seconds = totalSeconds;
    if (seconds > 0 || parts.empty()) parts.push_back(to_string(seconds) + " second");

    // 拼接结果
    stringstream result;
    for (size_t i = 0; i < parts.size(); ++i) {
        if (i > 0) result << " ";
        result << parts[i];
    }

    return result.str();
}

string convertDuration(const string& input) {
    istringstream iss(input);
    long long value;
    string unit;
    if (!(iss >> value >> unit)) {
        return "input error";
    }

    long long baseSeconds = unitToSeconds(unit);
    if (baseSeconds < 0) {
        return "unsupported unit";
    }

    long long totalSeconds = value * baseSeconds;
    return formatDuration(totalSeconds);
}

int main() {
    string line;
    cout << "input duration: ";
    getline(cin, line);

    string result = convertDuration(line);
    cout << result << endl;

    return 0;
}
