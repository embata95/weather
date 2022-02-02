function ShowData({ weather_data }) {
    let content = weather_data.map((curr_day) =>
    <tr key={weather_data.indexOf(curr_day)}>
      <td>
        {curr_day.date}
      </td>
      <td>
        {curr_day.day_name}
      </td>
      <td >
        {curr_day.min_temp}
      </td>
      <td>
        {curr_day.max_temp}
      </td>
    </tr>
    )
    if (!weather_data) {
      return <h1>No weather data currently, sorry!</h1>
    }
    return (
      <table className="weather_data_table">
        <thead>
          <tr>
            <th>
              Date
            </th>
            <th>
              Day
            </th>
            <th>
              Min
            </th>
            <th>
              Max
            </th>
          </tr>
        </thead>
        <tbody>
          {content}
        </tbody>
      </table>
      )
  }

export default ShowData;