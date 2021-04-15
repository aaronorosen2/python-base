import React, {useState} from "react";


const AddUser = ({addUser, setClickEventTotalUsers, clickEventTotalUsers, setUserModalVisible}) => {

    const [name, setName] = useState("")
    const [email, setEmail] = useState("")

    const handleChangeName = (e) => {
        let name = e.target.value;
        setName(name)
    }

    const handleChangeEmail = (e) => {
        setEmail(e.target.value)
    }


    const handleSubmit = (e) => {
        e.preventDefault()
        addUser({
            "name": name,
            "email": email,
        })
        setClickEventTotalUsers(clickEventTotalUsers + 1)
        setUserModalVisible(false)
    }


    return (
        <form onSubmit={handleSubmit} id="form">
            <div className="flex-wrapper">
                <div className="row mr-1">

                    <input onChange={handleChangeName} className="form-control m-1" id="name"
                           type="text" name="name"
                           placeholder="User Name"/>

                    <input className="form-control m-1"
                           id="email"
                           onChange={handleChangeEmail}
                           type="email" name="email"
                           placeholder="User Email"/>

                </div>
                <input id="submit" className="btn btn-primary" type="submit" name="Add"/>
            </div>
        </form>
    )
}

export default AddUser;