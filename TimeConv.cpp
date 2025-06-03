#include <iostream>
#include <string>
#include <sstream>

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
    string result;

    long long years = totalSeconds / YEAR;
    totalSeconds %= YEAR;

    long long months = totalSeconds / MONTH;
    totalSeconds %= MONTH;

    long long days = totalSeconds / DAY;
    totalSeconds %= DAY;

    long long hours = totalSeconds / HOUR;
    totalSeconds %= HOUR;

    long long minutes = totalSeconds / MINUTE;
    totalSeconds %= MINUTE;

    long long seconds = totalSeconds;

    if (years > 0) result += to_string(years) + "year";
    if (months > 0) result += to_string(months) + "month";
    if (days > 0) result += to_string(days) + "day";
    if (hours > 0) result += to_string(hours) + "hour";
    if (minutes > 0) result += to_string(minutes) + "minute";
    if (seconds > 0 || result.empty()) result += to_string(seconds) + "second";

    return result;
}

// 关键函数：输入原始字符串，输出格式化字符串
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
