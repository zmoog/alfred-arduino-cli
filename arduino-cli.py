# encoding: utf-8

import argparse
import json
import sys

from workflow import Workflow, ICON_WEB, web

log = None


def run_command(cmd):
    from invoke import run
    
    cmd = "./arduino-cli {cmd} --format json".format(cmd=cmd)

    result = run(cmd, hide=True, warn=True)
    if not result.ok:
        raise Exception(result.stdout)

    return json.loads(result.stdout)


def search_key_for_board(board):
    elements = []
    elements.append(board["name"])
    elements.append(board["FQBN"])
    return u" ".join(elements)
    
    
class Handler:

    def __init__(self, args, wf):
        self.args = args
        self.wf = wf

    def run(self):
        
        name = "handle_{command}_{subcommand}".format(command=self.args.command,
                                                      subcommand=self.args.subcommand)
        command = getattr(self, name, None)
        
        if not callable(command):
            raise Exception("Command not supported")
    
        command()        

    def handle_core_list(self):

        def wrapper():
            return run_command("core list")

        cores = self.wf.cached_data('cores', wrapper, max_age=120)

        if self.args.query:
            cores = self.wf.filter(self.args.query,
                                   boards,
                                   key=search_key_for_core,
                                   min_score=20)

        for core in cores:
            self.wf.add_item(title=core['ID'] + "@" + core['Installed'],
                             subtitle=core['Name'])

        # Send the results to Alfred as XML
        self.wf.send_feedback()
        
    def handle_board_listall(self):

        def wrapper():
            return run_command("board listall").get("boards", [])

        boards = self.wf.cached_data('boards', wrapper, max_age=120)

        if self.args.query:
            boards = self.wf.filter(self.args.query,
                                    boards,
                                    key=search_key_for_board,
                                    min_score=20)

        for board in boards:
            self.wf.add_item(title=board['name'],
                        subtitle=board['FQBN'],
                        icon=ICON_WEB)

        # Send the results to Alfred as XML
        self.wf.send_feedback()

    def handle_version_none(self):
        
        version = run_command("version")

        self.wf.add_item(title=version["VersionString"],
                         subtitle='version')
        self.wf.add_item(title=version["Commit"],
                         subtitle='Commit')
        self.wf.add_item(title=version["Status"],
                         subtitle='Status')

        
        # Send the results to Alfred as XML
        self.wf.send_feedback()
        
        
def main(wf):
  
    # build argument parser to parse script args and collect their
    # values
    parser = argparse.ArgumentParser()

    # add a required command and save it to 'command'
    parser.add_argument('command') 
    # add a required sub command and save it to 'sub_command'
    parser.add_argument('subcommand', nargs='?', default='none')
    # add an optional query and save it to 'query'
    parser.add_argument('query', nargs='?', default=None)

    # parse the script's arguments
    args = parser.parse_args(wf.args)

    Handler(args, wf).run()


if __name__ == u"__main__":
    wf = Workflow(libraries=["./libs"])
    log = wf.logger
    sys.exit(wf.run(main))
