import { BACKEND_URL } from '@/config/app';
import React from 'react';



export default async (req,res)=> {
  if(req.method === "POST"){

    const {name,email,password} = req.body

    const resAPI = await fetch(`${BACKEND_URL}/auth/user/`,{
      method:"POST",
      headers:{
        "content-type":"application/json"
      },
      body:JSON.stringify({email,name,password})
    })

    const data = await resAPI.json()
    if(resAPI.ok){
      res.status(200).json(data)
      return
    }else{
      res.status(400).json(data)
      return
    }

  }else{
    res.setHeader("Allowed",["POST"])
    res.status(400).json({
      "message":`${req.method} is not Allowed`
    })
    return
  }

}
