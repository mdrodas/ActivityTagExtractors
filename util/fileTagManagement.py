"""
Implementation for new tags extractor (crowded) using a list of files with the structure: _id; ratingTime; isDuplicate; keyword0; keyword1; keyword2; keyword3.
"""
import os
import util.FileManager as fm

if __name__ == "__main__":
    manager = fm()
    manager.writeResources()
