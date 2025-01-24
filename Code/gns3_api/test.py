import gns3_actions

if __name__ == '__main__':
    project_id = gns3_actions.get_project_id("localhost",'test' )

    response = gns3_actions.export_project("localhost", project_id)

    with open("response.gns3project", "wb") as f:
        f.write(response.content)