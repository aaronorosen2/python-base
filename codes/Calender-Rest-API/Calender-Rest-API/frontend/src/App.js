import React, {useEffect} from "react";
import {Calendar, dateFnsLocalizer} from "react-big-calendar";
import format from "date-fns/format";
import parse from "date-fns/parse";
import startOfWeek from "date-fns/startOfWeek";
import getDay from "date-fns/getDay";
import "react-big-calendar/lib/css/react-big-calendar.css";
import {Modal} from 'antd';
import 'antd/dist/antd.css';
import AddForm from "./add_event_form";
import AddUser from "./add_user";
import axios from 'axios';


const App = () => {

    const [visible, setVisible] = React.useState(false);
    const [confirmLoading, setConfirmLoading] = React.useState(false);
    const [clickedDate, setClickedData] = React.useState(null);
    const query = new URLSearchParams(window.location.search);
    const stadium = query.get('stadium')
    console.log('stadium='+stadium)

    const [selectedDay, setSelectedDay] = React.useState(null);
    const [selectedMonth, setSelectedMonth] = React.useState(null);
    const [selectedYear, setSelectedYear] = React.useState(null);
    const [selectedStadium, setSelectedStadium] = React.useState(null);
    const locales = {
        "en-US": require("date-fns/locale/en-US")
    };
    const localizer = dateFnsLocalizer({
        format,
        parse,
        startOfWeek,
        getDay,
        locales
    });
    const [myEventsList, setMyEventsList] = React.useState([]);

    const handleClick = (data) => {

        let date = data.start.getDate()
        let month = data.start.getMonth()
        let year = data.start.getFullYear()
        const query = new URLSearchParams(window.location.search);
        const stadiumid = query.get('stadium')
        setSelectedStadium(stadium)
        setSelectedDay(date)
        setSelectedMonth(month)
        setSelectedYear(year)

        setClickedData(year.toString() + "-" + (month + 1).toString() + "-" + date.toString())
        console.log(clickedDate)
        setVisible(true);
    }

    const handleOk = () => {
        setConfirmLoading(true);
        setVisible(false);
        setConfirmLoading(false);
    };

    const handleCancel = () => {
        setVisible(false);
    };

    const addEvent = (e) => {
        console.log(e)
        axios.post('https://api.dreampotential.org/bookingstadium/bookings/', e)
            .then(response => {
                console.log(response)
                setMyEventsList(
                    prevData => [...prevData, {
                        id: response.id,
                        start: new Date(selectedYear, selectedMonth, selectedDay),
                        end: new Date(selectedYear, selectedMonth, selectedDay),
                        title: response.data.name,
                        email: response.data.email,
                        phone: response.data.phone,
                        date: response.data.date,
                        start_time: response.data.start_time,
                        end_time: response.data.end_time,
                        stadium: 'ds'
                    }]
                )
            })
    }

    const addUser = (e) => {
        e['event'] = clickEventID
        console.log(e)
        axios.post("https://api.dreampotential.org/bookingstadium/user/assign/", e)
            .then(response => {
                setMyEventsList([])
                fetchEvents()
            })
    }


    const fetchEvents = () => {
        // setMyEventsList([]);
        axios.get('https://api.dreampotential.org/bookingstadium/api/bookings')
            .then(response => {
                    console.log(response.data)
                    response.data.forEach((response, index) => {
                        let date = response.date.split('-')
                        let year = parseInt(date[0])
                        let month = parseInt(date[1]) - 1
                        let day = parseInt(date[2])

                        console.log(year, month, day)

                        setMyEventsList(
                            prevData => [...prevData, {
                                id: response.id,
                                start: new Date(year, month, day),
                                end: new Date(year, month, day),
                                title: response.name,
                                email: response.email,
                                phone: response.phone,
                                date: response.date,
                                start_time: response.start_time,
                                end_time: response.end_time,
                                stadium: response.stadium,
                                total_users: response.total_users

                            }]
                        )
                    })
                }
            )
    }
    useEffect(() => {
        fetchEvents()
    }, [])


    const [clickEventID, setClickEventID] = React.useState('')
    const [clickEventName, setClickEventName] = React.useState('')
    const [clickEventEmail, setClickEventEmail] = React.useState('')
    const [clickEventPhone, setClickEventPhone] = React.useState('')
    const [clickEventDate, setClickEventDate] = React.useState(null)
    const [clickEventStartTime, setClickEventStartTime] = React.useState(null)
    const [clickEventEndTime, setClickEventEndTime] = React.useState(null)
    const [clickEventTotalUsers, setClickEventTotalUsers] = React.useState(null)
    const [clickEventStadium, setClickEventStadium] = React.useState(null)
    
    const [eventModalVisible, setEventModalVisible] = React.useState(false)
    const [eventConfirmLoading, setEventConfirmLoading] = React.useState(false);

    const handleEventOk = () => {
        setEventConfirmLoading(true);
        setEventModalVisible(false);
        setEventConfirmLoading(false);
    };

    const handleEventCancel = () => {
        setEventModalVisible(false);
    };

    const handleEventClick = (event) => {
        console.log(event)
        setClickEventID(event.id)
        setEventModalVisible(true);
        setClickEventName(event.title)
        setClickEventEmail(event.email)
        setClickEventPhone(event.phone)
        setClickEventDate(event.date)
        setClickEventStartTime(event.start_time)
        setClickEventEndTime(event.end_time)
        setClickEventTotalUsers(event.total_users)
        setClickEventStadium(event.stadium)
    }


    const [userModalVisible, setUserModalVisible] = React.useState(false);
    const [userConfirmLoading, setUserConfirmLoading] = React.useState(false);

    const handleUserOk = () => {
        setUserConfirmLoading(true);
        setUserModalVisible(false);
        setUserConfirmLoading(false);
    };

    const handleUserCancel = () => {
        setUserModalVisible(false);
    };

    return (
        <div className="App">
            <Calendar
                selectable={true}
                localizer={localizer}
                events={myEventsList}
                startAccessor="start"
                endAccessor="end"
                style={{height: 500}}
                onSelectEvent={event => handleEventClick(event)}
                onSelectSlot={(data) => handleClick(data)}
            />

            <Modal
                title="Add event"
                visible={visible}
                onOk={handleOk}
                confirmLoading={confirmLoading}
                onCancel={handleCancel}
            >
                <AddForm clickedDate={clickedDate} addEvent={addEvent} modalVisible={setVisible}/>
            </Modal>

            <Modal
                title="Event"
                visible={eventModalVisible}
                onOk={handleEventOk}
                confirmLoading={eventConfirmLoading}
                onCancel={handleEventCancel}
            >
                <p><b>Event:</b> {clickEventName}</p>
                <p><b>Email:</b> {clickEventEmail}</p>
                <p><b>Phone:</b> {clickEventPhone}</p>
                <p><b>Date:</b> {clickEventDate}</p>
                <p><b>Start Time:</b> {clickEventStartTime}</p>
                <p><b>End Time:</b> {clickEventEndTime}</p>
                 <p><b>Stadium:</b> {clickEventStadium}</p>
                <p><b>{clickEventTotalUsers}</b> user are attending</p>
                <button onClick={() => {
                    setUserModalVisible(true)
                }} className={"btn btn-primary"}>Attend
                </button>


            </Modal>

            <Modal
                title="Attend Event"
                visible={userModalVisible}
                onOk={handleUserOk}
                confirmLoading={userConfirmLoading}
                onCancel={handleUserCancel}
            >
                <AddUser addUser={addUser} setClickEventTotalUsers={setClickEventTotalUsers}
                         clickEventTotalUsers={clickEventTotalUsers} setUserModalVisible={setUserModalVisible}/>
            </Modal>
        </div>
    );
}

export default App;