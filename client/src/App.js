import { useState ,useEffect } from "react"
import logo from './logo.svg';
import './App.css';

function getCookie(name) {
  let cookieValue = null;
  console.log("cookie is :", typeof (document.cookie))
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


function App() { 

  const [token, setToken] = useState(null)
  const [response, setResponse] = useState("")


  useEffect(() => {
    try {
      let _token=localStorage.getItem("token")
      setToken(_token)
    } catch (error) {
      console.error(error)
    }
  }, [])
  
  let jwt_token = null

  const login = () => {

    fetch("/api/login/", {
      method: "post",
      headers: {
        "Content-Type": "application/json;charset=utf-8",
      },
      body: JSON.stringify({
        uname: "guru"
      })
    })
      .then((res) => res.json())
      .then((response) => {
        if (response.access_token) {
          setToken(response.access_token)
          localStorage.setItem("token",response.access_token)
        }
        setResponse(response)
      })
      .catch(err => {
        console.error(err)
        alert("error")
      })

  }

  const verifyLogin = () => {

    fetch("/api/verify_login/", {
      method: "post",
      headers: {
        "Content-Type": "application/json;charset=utf-8",
        'X-CSRFToken': getCookie("csrftoken"),
        "Authorization": token
      }
    })
      .then((res) => res.json())
      .then((response) => {
        setResponse(response)
      })
      .catch(err => {
        console.error(err)
        alert("error")
      })

  }

  const verifyLogin2 = () => {

    fetch("/api/verify_login/", {
      method: "post",
      headers: {
        "Content-Type": "application/json;charset=utf-8",
        'X-CSRFToken': getCookie("csrftoken"),
      },
      credentials: 'include'
    })
      .then((res) => res.json())
      .then((response) => {
        setResponse(response)
      })
      .catch(err => {
        console.error(err)
        alert("error")
      })

  }

  const logout = () => {
    fetch("/api/logout/", {
      method: "post",
      headers: {
        "Content-Type": "application/json;charset=utf-8",
        'X-CSRFToken': getCookie("csrftoken"),
      },
      credentials: 'include'
    })
      .then((res) => res.json())
      .then((response) => {
        setResponse(response)
      })
      .catch(err => {
        console.error(err)
        alert("error")
      })
  }


  const logout_from_all = () => {
    fetch("/api/logout_all/", {
      method: "post",
      headers: {
        "Content-Type": "application/json;charset=utf-8",
        'X-CSRFToken': getCookie("csrftoken"),
      },
      credentials: 'include'
    })
      .then((res) => res.json())
      .then((response) => {
        setResponse(response)
      })
      .catch(err => {
        console.error(err)
        alert("error")
      })
  }

  return (
    <div className="App">
      <div className="contents">
        <button onClick={login}>Login</button>
        <button onClick={verifyLogin}>Verify login by sending token as authorization header</button>
        <button onClick={verifyLogin2}>Verify login by sending token in http only cookie</button>

        <div className="break">
          {JSON.stringify(response)}
        </div>

      </div>
      <br />
      <div className="contents">
        <button onClick={logout}>Logout</button>
        <button onClick={logout_from_all}>Logout from all</button>
      </div>
    </div>
  );
}

export default App;
