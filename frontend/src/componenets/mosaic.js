import React, { useState, useEffect } from "react";
import axios from 'axios';
import { Button, Form, Image, Header, Container } from "semantic-ui-react";
import '../App.css'

export default function Mosaic() {

    const [image, setImage] = useState({
        data: {
            name:'image',
            image: null,
            mosaic: null
        },
        images: [],
        info: "block",
        loader: "none",
        display: "none",
        message: "",
        gallery: []
    });


    const handleImageChange = (e) =>{
        setImage({
            ...image,
            data: {
                ...image.data.name,
                image: e.target.files[0],
                ...image.data.mosaicc
            }
        })
    };

    const handleSourceImageChange = (e) => {
        setImage({
            ...image,
            images: e.target.files
        })
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(image);
        postImageTest();
    } 

    function postImageTest(){
        setImage({
            ...image,
            info: "none",
            display: "block"
        })
    }

    async function postImage() {
        setImage({
            ...image,
            info: "none",
            display: "block",
            loader: "block"
        })
        let form_data1 = new FormData();
        form_data1.append('image', image.data.image, image.data.image.name);
        form_data1.append('name', image.data.name);
        

        const headers = {
            headers: {
                'content-type': 'multipart/form-data'
            }
        }

        var i = 0;
        const tot = parseInt(image.images.length);
        const images = Array.from(image.images)
        console.log(images)

        for (const img of images) {
            let form_data2 = new FormData();
            form_data2.append('image', img, img.name);
            form_data2.append('album', 1 );

            const res1 = await axios.post( 'http://localhost:8000/api/images/', form_data2, headers);
            if (res1.status > 400) {
                return setImage(() => {
                    return { placeholder: "Something went wrong!" };
                });
            }
            console.log(res1)

            i += 1;

            setImage({
                ...image,
                info: "none",
                display: "block",
                loader: "block",
                message: `...Finished Processing ${i} out of ${tot} files.`
            })

        }

        setImage({
            ...image,
            info: "none",
            display: "block",
            loader: "block",
            message: 'Creating Mosaic. This will take a few seconds...'
        })

        const res = await axios.post('http://localhost:8000/api/newmosaic/', form_data1, headers);
        if (res.status > 400) {
            return setImage(() => {
                return { placeholder: "Something went wrong!" };
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
                display: "block",
            };
        });
    }

    return (
        <React.Fragment>
            <div>
                <Header as='h3'>Use Your Images</Header>
            </div>
    
            <Container textAlign="center" >
                                <div class="info" style = {{display: image.info}}>
                                    <p>Upload image files for the main image and the mosiac images.</p> 
                                         <p>The more images the better.</p>
                                </div>
                                <div class="img" style={{display: image.display}}>
                                    <div class="loader-wrapper" id="toggle2" style = {{display:image.loader}}>
                                        <div class = "first">
                                            <span class="loader"><span class="loader-inner"></span></span>
                                        </div>
                                        <div class = "second">
                                            <p>{image.message}</p>
                                        </div>
                                    </div> 
                                    <section class="box" >
                                        <p color="white">This feature is comming soon... </p>
                                        <div class="dn-btn" >
                                            <a href="" target="_blank">Thankyou</a>
                                        </div>
                                    </section>
                                </div>
                            </Container>
                            <Form onSubmit={handleSubmit} style = {{display:image.info}}>
                                <Form.Group>
                                        <Form.Input
                                            label="Main Image"  
                                            type="file"
                                            float="left"
                                            id="image"
                                            accept="image/png, image/jpeg, image/jpg" 
                                            onChange={handleImageChange} required/>
                                        <Form.Input
                                            label="Mosaic Images"
                                            type="file"
                                            float="left"
                                            id="image"
                                            accept="image/png, image/jpeg, image/jpg"
                                            onChange={handleSourceImageChange} required multiple/>
                                </Form.Group>
                                <Button float color="teal" type="submit">Create Mosaic</Button>
                            </Form>
                        </React.Fragment>
    )
}
