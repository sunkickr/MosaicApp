import React from 'react'
import { Header, Menu } from "semantic-ui-react";
import { Link } from 'react-router-dom';
import '../App.css'

export default function Navbar() {

    // const topFunction = () => {
    //     document.body.scroll.scrollTop = 0; // For Safari
    //     document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
    // }

    const handleRefresh = () => {
        window.location.reload();
    }

    return (
        <Menu pointing secondary>
        <Menu.Item
            name='editorials'
            active=""
            onClick={handleRefresh}
            >
            <Header color="teal" as='h1'>MosaicApp</Header>
        </Menu.Item>
        <Menu.Menu >
        <Menu.Item
            name='editorials'
            active=""
            >
            <Link to="/" color="black">Quick Mosaic</Link>
        </Menu.Item>
        <Menu.Item
            name='reviews'
            active=""
            >
            <Link to="/mosaic">Use Your Images</Link>
        </Menu.Item>
        </Menu.Menu>
    </Menu>
    )
}
