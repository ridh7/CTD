import React from 'react'
import { Link, withRouter } from 'react-router-dom'

class Main extends React.Component {
    handleSubmit(e) {
        
    }

    render() {
        return (
            <div>
                <div className="navig "></div>
                <div className="centerbox">
                    <div className="title">Instructions</div>
                    <div className="content">
                        <ul>
                            <li>This round comprises of 6 questions</li>
                            <li>All questions have marking scheme +4,-2</li>
                            <li>Placeholder</li>
                            <li>Placeholder</li>
                        </ul>
                    </div>
                    <div className="proceed">
                        <form onSubmit={this.handleSubmit}>
                            <button><Link to="/Coding">PROCEED</Link></button>
                        </form>
                    </div>
                </div>
                <div className=" footer">© PICT IEEE STUDENT BRANCH</div>
            </div>
        )
    }
}

export default withRouter(Main)