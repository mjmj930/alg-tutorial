#include <iostream>
#include <string>
#include <sstream>
#include <map>

using namespace std;

// 时间单位对应的秒数，1 month 取30天，1 year 取365天
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
    return -1; // 不支持的单位
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

int main() {
    string line;
    cout << "input duartion:";
    getline(cin, line);

    istringstream iss(line);
    long long value;
    string unit;
    iss >> value >> unit;

    long long baseSeconds = unitToSeconds(unit);
    if (baseSeconds < 0) {
        cout << "unsupport unit" << endl;
        return 1;
    }

    long long totalSeconds = value * baseSeconds;

    string output = formatDuration(totalSeconds);
    cout << output << endl;

    return 0;
}
