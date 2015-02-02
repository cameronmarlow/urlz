//
//  ViewController.swift
//  URLer
//
//  Created by Jeffery Bennett on 2/1/15.
//  Copyright (c) 2015 PermanentRecord. All rights reserved.
//

import UIKit
import CoreData

class ViewController: UIViewController {

    
    /** Auth/Signup View **/
    @IBOutlet weak var auth_view: UIView!
    
    @IBOutlet weak var login_uname: UITextField!
    @IBOutlet weak var login_pass: UITextField!
    @IBOutlet weak var login_btn: UIButton!
    
    @IBOutlet weak var signup_uname: UITextField!
    @IBOutlet weak var signup_realname: UITextField!
    @IBOutlet weak var signup_email: UITextField!
    @IBOutlet weak var signup_pass: UITextField!
    @IBOutlet weak var signup_btn: UIButton!
    
    
    /** Constants **/
    let API_ENDPOINT : String = "http://urler.herokuapp.com"
    
    
    /** CORE DATA **/
    lazy var managedObjectContext : NSManagedObjectContext? = {
        let appDelegate = UIApplication.sharedApplication().delegate as AppDelegate
        if let managedObjectContext = appDelegate.managedObjectContext {
            return managedObjectContext
        } else {
            return nil
        }
     }()

    
    override func viewDidLoad() {
        super.viewDidLoad()
        //self.auth_view.hidden = true
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func onLoginPress(sender: UIButton) {
        if (!self.login_uname.text.isEmpty &&
            !self.login_pass.text.isEmpty) {
                self.login(self.login_uname.text, password: self.login_pass.text)
        } else {
            //TODO - show alert.
        }
    }
    
    func login(username: String, password:String) {
        println("LOGGING IN WITH (" + username + "/" + password + ")")
        let login_obj:[String:AnyObject] = [
            "username":username,
            "password":password
        ]
        
        auth_view.alpha = 0.25;
        
        let login_json  = JSON(login_obj)
        let login_str   = login_json.toString()
        let login_url   = NSURL(string: API_ENDPOINT + "/api/login")
        let request     = NSMutableURLRequest(URL: login_url!)
        request.setValue("application/json", forHTTPHeaderField: "Content-type");
        request.HTTPMethod  = "POST"
        
        let data        = login_str.dataUsingEncoding(NSUTF8StringEncoding)
        let task        = NSURLSession.sharedSession().uploadTaskWithRequest(request, fromData: data, completionHandler: { (data:NSData!, response:NSURLResponse!, error: NSError!) -> Void in
            if (error == nil) {
                let rspDict:NSDictionary = NSJSONSerialization.JSONObjectWithData(data, options: nil, error: nil) as NSDictionary
                println(rspDict)
            }
        })
        task.resume()
    }
    
    

    @IBAction func onSignupPress(sender: UIButton) {
        if (!self.signup_uname.text.isEmpty &&
            !self.signup_pass.text.isEmpty &&
            !self.signup_realname.text.isEmpty &&
            !self.signup_email.text.isEmpty) {
                
                let signup_obj:[String:AnyObject] = [
                    "username":self.signup_uname.text,
                    "name":self.signup_realname.text,
                    "email":self.signup_email.text,
                    "password":self.signup_pass.text
                ]
                
                let signup_json  = JSON(signup_obj)
                let signup_str   = signup_json.toString()
                let signup_url   = NSURL(string: API_ENDPOINT + "/api/user")
                let request     = NSMutableURLRequest(URL: signup_url!)
                request.setValue("application/json", forHTTPHeaderField: "Content-type");
                request.HTTPMethod  = "POST"
                
                auth_view.alpha = 0.25;
                
                let data        = signup_str.dataUsingEncoding(NSUTF8StringEncoding)
                let task        = NSURLSession.sharedSession().uploadTaskWithRequest(request, fromData: data, completionHandler: { (data:NSData!, response:NSURLResponse!, error: NSError!) -> Void in
                    if (error == nil) {
                        let rspDict:NSDictionary = NSJSONSerialization.JSONObjectWithData(data, options: nil, error: nil) as NSDictionary
                        if (rspDict["message"] != nil) {
                            //Duplicate user.
                        } else {
                            //New user. Log in.
                            //Return to main thread & log in.
                            dispatch_async(dispatch_get_main_queue(), { () -> Void in
                                self.login(self.signup_uname.text, password:self.signup_pass.text)
                            });
                            
                        }
                    }
                })
                task.resume()
            
        } else {
            //TODO - show alert.
        }
    }
    
    
    
 
    
}

