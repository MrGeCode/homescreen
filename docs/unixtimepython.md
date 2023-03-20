Unix timestamp

```
import datetime

unix_timestamp = 1679263200
readable_time = datetime.datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')

print(readable_time)
```