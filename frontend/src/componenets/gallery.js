import React from 'react'
import { Image } from "semantic-ui-react";
import '../App.css'

export default function Gallery(props) {

    return(
        <div className="img">
        <section class="box" >
            <Image src={props.mosaic}/>
            <div class="dn-btn" >    
                <a href={props.mosaic} target="_blank">Download and View</a>
            </div>
        </section>
        </div>
    )
}