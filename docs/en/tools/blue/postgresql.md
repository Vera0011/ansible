---
layout: default
title: PostgreSQL
parent: Tools
grand_parent: English
---

# PostgreSQL

## Introduction

PostgreSQL is a relational database system. It is used to store information and data, using the language SQL.</br>
This tool belongs to the `Blue Team` section.

## Implementation

The implementation of this tool in Ansible is as follows:

1. PostgreSQL is installed and configured on the specified host
2. A dedicated user and group are used to run PostgreSQL. They are automatically configured when installing the package
3. There are different modules that can be loaded:
   - User creation
   - Database creation
   - Oauth implementation (for future implementations, not available)
   - WAL and replica implementation
4. If users are created, a file is generated (with their credentials) [here](../../../../generated/postgresql_users.txt).

## Usage

1. Run the playbook (instructions can be found [here](../../../../roles/postgresql/README.md))
2. After the installation and configuration, you will have access to the database!
