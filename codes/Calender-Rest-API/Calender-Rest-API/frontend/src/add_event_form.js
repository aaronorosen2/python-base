import React, {useState} from "react";
import TimePicker from 'react-time-picker'


const AddForm = ({clickedDate, addEvent, modalVisible}) => {

    const [name, setName] = useState("")
    const [email, setEmail] = useState("")
    const [phone, setPhone] = useState("")
    const [start_time, setStartTime] = useState('12:00')
    const [end_time, setEndTime] = useState('12:00')
    const query = new URLSearchParams(window.location.search);
    const stadiumid = query.get('stadium')
    const handleChangeName = (e) => {
        let name = e.target.value;
        setName(name)
    }

    const handleChangeEmail = (e) => {
        setEmail(e.target.value)
    }

    const handleChangePhone = (e) => {
        setPhone(e.target.value)
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        addEvent({
            "name": name,
            "email": email,
            "phone": phone,
            "date": clickedDate,
            "start_time": start_time,
            "end_time": end_time,
            "stadium":stadiumid
        })
        modalVisible(false)
    }


    return (
        <form onSubmit={handleSubmit} id="form">
            <div className="flex-wrapper">
                <div className="row mr-1">

                    <input onChange={handleChangeName} className="form-control m-1" id="name"
                           type="text" name="name"
                           placeholder="Event Name"/>

                    <input className="form-control m-1"
                           id="email"
                           onChange={handleChangeEmail}
                           type="email" name="email"
                           placeholder="email"/>

                    <input onChange={handleChangePhone} className="form-control m-1" id="phone"
                           type="text" name="phone"
                           placeholder="Phone Number"/>

                    <input className="form-control m-1" disabled value={clickedDate}/>

                    <div className="col-md-12 m-1">
                        <label htmlFor="startdate">Start Time</label>
                        <TimePicker id='startdate'
                                    onChange={setStartTime}
                                    value={start_time}
                        />
                    </div>

                    <div className="col-md-12 m-1">
                        <label htmlFor="enddate">End Time</label>
                        <TimePicker id='enddate'
                                    onChange={setEndTime}
                                    value={end_time}
                        />
                    </div>


                </div>
                <input id="submit" className="btn btn-warning" type="submit" name="Add"/>
            </div>
        </form>
    )
}

export default AddForm;