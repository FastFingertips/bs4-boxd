from methods.system_ import fileRenamer
from methods.log_ import preCmdErr, preCmdInfo
from methods.file_ import loadJsonFile, dumpJsonFile, fileExists
from constants.project import (SESSIONS_FILE_NAME, SESSION_DICT_KEY,
                               SESSION_PROCESSES_KEY, SESSION_START_KEY,
                               SESSION_LAST_KEY, SESSION_FINISHED_KEY)
import json
import os

current_pid = str(os.getpid())

# -- SESSIONS --

def createSession(app_id) -> None:
    # If the session file does not exist, it is created.
    jsonObject = {
        SESSION_DICT_KEY: {
            current_pid: {
                SESSION_START_KEY: app_id,
                SESSION_LAST_KEY: app_id,
                SESSION_PROCESSES_KEY: {
                    app_id: {
                        SESSION_FINISHED_KEY: False
                    }
                }
            }
        }
    }
    dumpJsonFile(SESSIONS_FILE_NAME, jsonObject)

def endSession(current_hash) -> None:
    # Current process is marked as finished.
    sessionRecords = loadJsonFile(SESSIONS_FILE_NAME)
    sessionRecords[SESSION_DICT_KEY][current_pid][SESSION_PROCESSES_KEY][current_hash][SESSION_FINISHED_KEY] = True
    dumpJsonFile(SESSIONS_FILE_NAME, sessionRecords)

def newSession(start_hash) -> None:
    sessionRecords = loadJsonFile(SESSIONS_FILE_NAME)
    if current_pid in sessionRecords[SESSION_DICT_KEY]:
        # If the process is already in the session file, the session is updated.
        updateSession(start_hash)
    else:
        # If the process is not in the session file, a new session is created.
        sessionRecords[SESSION_DICT_KEY] |= {
            current_pid: {
                SESSION_START_KEY: start_hash,
                SESSION_LAST_KEY: start_hash,
                SESSION_PROCESSES_KEY: {
                    start_hash: {SESSION_FINISHED_KEY: False}
                }
            }
        }
        dumpJsonFile(SESSIONS_FILE_NAME, sessionRecords)

def updateSession(current_session):
    sessionRecords = loadJsonFile(SESSIONS_FILE_NAME)
    sessionRecords[SESSION_DICT_KEY][current_pid][SESSION_LAST_KEY] = current_session
    sessionRecords[SESSION_DICT_KEY][current_pid][SESSION_PROCESSES_KEY] |= {
        current_session: {
            SESSION_FINISHED_KEY: False
            }
        }

    dumpJsonFile(SESSIONS_FILE_NAME, sessionRecords)

def sessionCreator(app_id):
    try:
        # If the file does not exist, it will create a new one.
        print(f'{preCmdInfo}New session file creating...', end=' ')
        createSession(app_id)
        print(f'successfully.')
    except:
        print(f'failed.')
        raise Exception(f'{preCmdErr}Session file could not be created.')

def sessionBackup():
    try:
        # last session file backup
        print(f'{preCmdInfo}Session file backup...', end=' ')
        fileRenamer(SESSIONS_FILE_NAME, f'backup_broken_{SESSIONS_FILE_NAME}')
        print(f'successfully.') # backup successfully
    except:
        print(f'failed.') # backup failed
        raise Exception(f'{preCmdErr}Last session file could not be backup.')

def addSession(start_hash):
    try:
        # add new session
        print(f'{preCmdInfo}Starting new session...', end=' ')
        newSession(start_hash)
        print(f'successfully.') # add new session successfully
    except json.decoder.JSONDecodeError: 
        # If the file is broken or empty, the file will be backed up and a new one will be created.
        print(f'failed.') # add new session failed
        sessionBackup()
        sessionCreator(start_hash)

def startSession(start_hash) -> None:
    print(f'{preCmdInfo}Session file checking...', end=' ')
    if fileExists(SESSIONS_FILE_NAME):
        # If the session file exists, the session is started.
        print(f'successfully.') # checking successfully
        addSession(start_hash)
    else:
        print(f'failed.') # checking failed
        sessionCreator(start_hash)