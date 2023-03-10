import { BACKEND_URL } from '@/config/app';
import React from 'react';
import cookie from 'cookie';


export default async(req,res) => {
  if(req.method === "POST"){

    const {email,password} = req.body

    const resAPI = await fetch(`${BACKEND_URL}/auth/jwt/create/`,{
      method:"POST",
      headers:{
        "content-type":"application/json"
      },
      body: JSON.stringify({email,password})
    })

    const data = await res.json()

    if(res.ok){
      res.setHeader("Set-Cookie",[
        cookie.serialize("refresh_token",data.refresh,{
          httpOnly:true,
          secure: process.env.NODE_ENV !== "development",
          maxAge: 60*60*48,
          sameSite:"strict",
          path: "/"
        }),
        cookie.serialize("access_token",data.access,{
          httpOnly:true,
          secure: process.env.NODE_ENV !== "development",
          maxAge: 120,
          sameSite:"strict",
          path: "/"
        }),
      ])
      res.status(200).json({})
      return

    }else{
      res.status(401).json(data)
      return
    }

  }else{
    res.setHeader("Allowed",["POST"])
    res.status(400).json({
      "message": `${req.method} is Not Allowed`
    })
    return
  }
}
