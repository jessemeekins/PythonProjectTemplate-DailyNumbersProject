function displayTime() {
    var date = new Date();
    var dayOfWeek = date.toLocaleDateString('en-US', { weekday: 'long' });
    var month = date.toLocaleDateString('en-US', { month: 'long' });
    var day = date.toLocaleDateString('en-US', { day: 'numeric' });
    var year = date.toLocaleDateString('en-US', { year: 'numeric' });
    var hour = date.getHours();
    var minute = date.getMinutes();
    var second = date.getSeconds();
    var ampm = hour >= 12 ? 'pm' : 'am';
    hour = hour % 12;
    hour = hour ? hour : 12;
    minute = minute < 10 ? '0' + minute : minute;
    second = second < 10 ? '0' + second : second;
    var time = hour + ':' + minute + ':' + second + ' ' + ampm;
    var dateString = dayOfWeek + ', ' + month + ' ' + day + ', ' + year;
    document.getElementById('clock').innerHTML = dateString + ' ' + time;
    setTimeout(displayTime, 1000);
  }
  displayTime();