import React from 'react'
import axios from 'axios'


class Body extends React.Component {
    state = {
        post: null
    }
    componentDidMount() {
        let id=this.props.match.params.post_id;
        axios.get('api/question/1/')
            .then(res => {
                this.setState({
                    post: res.data
                })
            })
    }

    render() {
        const post = this.state.post ? (
            <div>
                <p>{this.state.post.questionTitle}</p>
            </div>

        ) : (
                <p>Loading Page Please Wait !!!</p>
            )

        return (
            <section className=" container-fluid bigbody">

                <div className="row BodY">
                    <div className="insideBody mt-3">
                        <div className="score">SCORE</div>
                        <div className="scoreval "></div>

                        <div className="custom-file choose" >
                            <input type="file" className="custom-file-input choosefile" id="customFile" name="filename" />
                            <label className="custom-file-label" htmlFor="customFile" >Choose file</label>
                        </div>
                    </div>
                    <div className="row insidecenterbody mt-3">
                        <textarea className="text" value={post} readOnly onClick="" />
                        {/* <div className="AceEditor">
                            <div id="editor"></div>
                        </div> */}

                    </div>
                    <div className="insideBody mt-3 row">
                        <div className="radiobox"><input type="radio" /></div>
                        <div className="Cbox">C</div>
                        <div className="radiobox"><input type="radio" /></div>
                        <div className="Cbox">C++</div>
                        <div className="loadbox "><button className="submit" name="buffer">LOAD BUFFER</button></div>
                        <div className="submitbox "><button className="submit" name="Submit">SUBMIT</button></div>

                    </div>


                </div>
            </section>
        )
    }
}



export default Body