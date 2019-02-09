import React from 'react'
import { Link, withRouter } from 'react-router-dom'



const Navbar = () => {

    return (
        <nav className="navig navbar navbar-expand-lg">
            <div className="row">
                <div className="head">CODING PAGE</div>
                <div className="row bigbuttonbox">
                    <div className="buttonbox">
                        <button className="but1"><Link to="/Question">QUESTION HUB</Link></button>
                    </div>
                    <div className="buttonbox">
                        <button className="but1"><Link to="/Leaderboard">LEADERBOARD</Link></button>
                    </div>
                    <div className="buttonbox">
                        <button className="but1"><Link to="/contact">LOG OUT</Link></button>
                    </div>
                </div>
            </div>
        </nav>
    )
}

export default withRouter(Navbar)
