import { BACKEND_URL } from "@/config/app";
import cookie from "cookie";


export default async (req,res)=>{
  if(req.method === "GET"){
    if(!req.headers.cookie){
      res.status(401).json({message: "Not authorized"})
      return
    }

    let {refresh_token,access_token} = cookie.parse(req.headers.cookie)

    if(!refresh_token){
      res.status(401).json({message:"Not Authorized"})
      return
    }

    if(!access_token){
      // refresh the  access_token
      const refreshRes = await refreshToken(req,res)

      if(refreshRes){
        access_token = refreshRes
      }else{
        res.status(401).json({message:"Not Authorized"})
        return;
      }
    }

    let resAPI = await fetch(`${BACKEND_URL}/auth/users/me/`,{
      method:"GET",
      headers: {
        "content-type":"application/json",
        Authorization: `Token ${access_token}`
      }
    })

    if(resAPI.ok){
      const user = await resAPI.json()

      res.status(200).json({user})

      return user
    }else{
      res.status(401).json({})
      return
    }

  }else{
    res.setHeader("Allowed",["GET"])
    res.status(403).json({message:`Method ${req.method} is not allowed`})
    return
  }
}