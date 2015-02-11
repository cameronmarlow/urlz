//
//  URLer.swift
//  URLer
//
//  Created by Jeffery Bennett on 2/9/15.
//  Copyright (c) 2015 PermanentRecord. All rights reserved.
//

import Foundation
import CoreData

class User: NSManagedObject {

    @NSManaged var username: String
    @NSManaged var name: String
    @NSManaged var password: String
    @NSManaged var auth_token: String
    @NSManaged var email: String

}
