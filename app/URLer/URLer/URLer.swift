//
//  URLer.swift
//  URLer
//
//  Created by Jeffery Bennett on 1/26/15.
//  Copyright (c) 2015 PermanentRecord. All rights reserved.
//

import Foundation
import CoreData

class URLer: NSManagedObject {

    @NSManaged var username: String
    @NSManaged var password: String
    @NSManaged var auth_token: String

}
