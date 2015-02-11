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
        managedObjectContext;
        
        //println(managedObjectContext!)
        self.auth_view.hidden = true
        let user:User? = self.getUser()
        if (user != nil) {
            //We have a pre-auth'd user.
        } else {
            
        }
        
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
        
        //Create you's k/v pairs for logging in.
        let login_obj:[String:AnyObject] = [
            "username":username,
            "password":password
        ]
        
        self.callAPI("/api/login", data: login_obj, { (data:NSData!, response:NSURLResponse!, error: NSError!) -> Void in
            if (error == nil) {
                let rspDict:NSDictionary = NSJSONSerialization.JSONObjectWithData(data, options: nil, error: nil) as NSDictionary
                let authToken: String = rspDict["auth_token"] as String
                let user:User? = self.getUser()
                if (user != nil) {
                    //We have a pre-stored user.  Update their auth token
                    println("Existing user")
                    println(user?.auth_token)
                    user?.auth_token = authToken
                    println("New auth token:" + authToken)
                    self.persistContext()
                } else {
                    println("Creating user")
                    println("Username: " + self.login_uname.text)
                    println("Password: " + self.login_pass.text)
                    println("Auth token: " + authToken)
                    //No user.  Create one.
                    let newUser = NSEntityDescription.insertNewObjectForEntityForName("User", inManagedObjectContext: self.managedObjectContext!) as User
                    newUser.username    = self.login_uname.text
                    newUser.password    = self.login_pass.text
                    newUser.auth_token  = authToken
                    self.persistContext()
                }
            }
        })
    }
    
    func getUser() -> User? {
        let fetchRequest = NSFetchRequest(entityName: "User")
        if let fetchResults = managedObjectContext!.executeFetchRequest(fetchRequest, error: nil) as? [User] {
            if (fetchResults.count > 0) {
                println("WE GOT ONE")
                return fetchResults[0] as User
            } else {
                println("No users stored.")
                return nil
            }
        } else {
            println("Negative, ghostrider.")
            return nil;
        }
    }
    
    //Tell the context to save the current state.
    func persistContext() {
        var appDel : AppDelegate = (UIApplication.sharedApplication().delegate as AppDelegate)
        var context : NSManagedObjectContext = appDel.managedObjectContext!
        context.save(nil)
    }
    
    func callAPI(method: String?, data: AnyObject?, completionHandler: ((NSData!, NSURLResponse!, NSError!) -> Void)?) {
        
        //Set up the data.  First, convert it to JSON, then to a string.
        let request_str     = JSON(data!).toString()
        //Encode the string as UTF-8 data.
        let data = request_str.dataUsingEncoding(NSUTF8StringEncoding)
        
        //Make the request object.
        let request_url     = NSURL(string: API_ENDPOINT + method!)
        let request         = NSMutableURLRequest(URL: request_url!)
        
        //Set the headers / method.
        request.setValue("application/json", forHTTPHeaderField: "Content-type")
        request.HTTPMethod  = "POST"
        
        //Make the request.
        
        //Get access to the app's shared session singleton.
        let session     = NSURLSession.sharedSession()
        let task        = session.uploadTaskWithRequest(request, fromData: data, completionHandler)
        task.resume();
    }
    
   
    
    @IBAction func onSignupPress(sender: UIButton) {
        if (!self.signup_uname.text.isEmpty &&
            !self.signup_pass.text.isEmpty &&
            !self.signup_realname.text.isEmpty &&
            !self.signup_email.text.isEmpty) {
                
                //Create k/v pairs for signing up.
                let signup_obj:[String:AnyObject] = [
                    "username":self.signup_uname.text,
                    "name":self.signup_realname.text,
                    "email":self.signup_email.text,
                    "password":self.signup_pass.text
                ]
                
                self.callAPI("/api/user", data: signup_obj, { (data:NSData!, response:NSURLResponse!, error: NSError!) -> Void in
                    if (error == nil) {
                        let rspDict:NSDictionary = NSJSONSerialization.JSONObjectWithData(data, options: nil, error: nil) as NSDictionary
                        if (rspDict["message"] != nil) {
                            //Duplicate user.
                            println("Sign up - Duplicate user.")
                        } else {
                            println("Sign up - Success.")
                            //New user. Log in.
                            //Return to main thread & log in.
                            dispatch_async(dispatch_get_main_queue(), { () -> Void in
                                self.login(self.signup_uname.text, password:self.signup_pass.text)
                            });
                            
                        }
                    }
                })
                
        } else {
            //TODO - show alert.
        }
    }
    
    
    
    
    
}

