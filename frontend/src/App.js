import React, { useState} from "react";
import { BrowserRouter as Router, Route } from 'react-router-dom';
import axios from 'axios';
import { Segment, Form, Image, Header, Container, Button } from "semantic-ui-react";
import Navbar from './componenets/navbar'
import Gallery from './componenets/gallery'
import Mosaic from './componenets/mosaic'
import './App.css'


axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

const handleRefresh = () => {
    window.location.reload();
}

function App() {
    const [image, setImage] = useState({
        data: {
            name:'image',
            image: null,
            mosaic: null
        },
        info: "block",
        loader: "none",
        display: "none",
        placeholder: "none",
        gallery: [
            "static/mosaic/mosaic1.jpg",
            "static/mosaic/mosaic2.jpg",
            "static/mosaic/mosaic3.jpg",
            "static/mosaic/mosaic4.jpg",
            "static/mosaic/mosaic5.jpg",
            "static/mosaic/mosaic6.jpeg",
            
        ]
    });

    const handleImageChange = (e) =>{
        setImage({
            ...image,
            data: {
                ...image.data.name,
                image: e.target.files[0],
                ...image.data.mosaic
            }
        })
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(image);
        postImage();
    }   

    // async function getImage() {
    //     const res = await axios.get('http://localhost:8000/api/mosaic/');
    //     if (res.status > 400) {
    //         return setImage(() => {
    //             return { placeholder: "Something went wrong!" };
    //         });
    //     }
    //     const mosaic = res.data.map(data => data.mosaic);
    //     console.log(res.data);
    //     console.log(mosaic);
    //     setImage({
    //         ...image,
    //         gallery: mosaic
    //     })
    //     console.log(image.gallery)
    // }

    async function postImage() {
        setImage({
            ...image,
            info: "none",
            display: "block",
            loader: "block"
        })
        let form_data = new FormData();
        form_data.append('image', image.data.image, image.data.image.name);
        form_data.append('name', image.data.name);
        const headers = {
            headers: {
                "X-CSRFToken": csrftoken,
                'content-type': 'multipart/form-data',
            }
        }
        const res = await axios.post('/api/mosaic/', form_data, headers);
        if (res.status > 400) {
            setImage(() => {
                return { 
                    ...image,
                    info: "none",
                    loaded: "none",
                    display: "block",
                    placeholder: "block" };
            });
        }

        setImage(() => {
            return {
                ...image,
                data: {
                    name: res.data.name,
                    image: res.data.image,
                    mosaic: res.data.mosaic 
                },
                info: "none",
                loaded: "none",
                display: "block"
            };
        });
    }

    return (
        <Router>
        <div className="App">
            <Segment style={{width:600}}>
                <Navbar />
                <div className="scroll">
                    <Route exact path="/" render={props => (
                        <React.Fragment>
                            <div >
                                <Header as='h3'>Quick Mosaic</Header>
                            </div>
                            <Container textAlign="center" >
                                <div class="info" style = {{display: image.info}}>
                                    <p>Upload an image file to create a mosaic</p>
                                </div>
                                <div class="img" style={{display: image.display}}>
                                    <div class="loader-wrapper" id="toggle2" style = {{display:image.loader}}>
                                        <div class = "first">
                                            <span class="loader"><span class="loader-inner"></span></span>
                                        </div>
                                        <div class = "second">
                                            <p>Creating Mosaic. This will take a few seconds...</p>
                                        </div>
                                    </div> 
                                    <section class="box" >
                                        <Image src={image.data.mosaic}/>
                                        <div style = {{display: image.placeholder}}>
                                            <p>Somthing went wrong! Please reload the page and try again.</p>
                                        </div>
                                        <div class="dn-btn" >
                                            <a href={image.data.mosaic} target="_blank">Download and View</a>
                                        </div>
                                        <div class="btn">
                                            <Button fluid onClick={handleRefresh}>Make Another Mosaic</Button>
                                        </div>
                                    </section>
                                </div>
                            </Container>
                            <Form onSubmit={handleSubmit} style = {{display:image.info}}>
                                <Form.Group>
                                        <Form.Input type="file"
                                            float="left"
                                            id="image"
                                            accept="image/png, image/jpeg, image/jpg" 
                                            onChange={handleImageChange} required/>
                                        <Form.Button color="teal" type="submit">Create Mosaic</Form.Button>
                                </Form.Group>
                            </Form>
                        </React.Fragment>
                    )} />
                    <Route path="/mosaic" component={Mosaic} />
                    <Container padding="1rem">
                        <div class="gallery">
                            <Header as='h3'>Mosaic Gallery</Header>
                        </div>
                        <div>
                            {image.gallery.map((mosaic, index) => (
                                <Gallery
                                    key={index}
                                    index={index}
                                    mosaic={mosaic}
                                    />
                                ))}
                        </div>
                    </Container>
                </div>
            </Segment>
        </div>
        </Router> 
    );
}

export default App;

