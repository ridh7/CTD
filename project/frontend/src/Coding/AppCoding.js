import React from 'react'
import Navbar from '../components/Navbar'
import Body from '../components/Body'
import Footer from '../components/Footer'
import {BrowserRouter, Route, Switch} from 'react-router-dom'
import Question from '../Question/Question';
import Leaderboard from '../Leaderboard/Leaderboard';


function AppCoding() {  


    return (
        <BrowserRouter>
            <div>
                <Navbar />
                <Switch>
                    <Route exact path='/Question' component={Question} />
                    <Route path='/Leaderboard' component={Leaderboard} />
                    <Route path='/Coding' component={Body} />
                </Switch>
                <Footer />
            </div>
        </BrowserRouter>


    )

}

export default AppCoding