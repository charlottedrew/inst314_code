from argparse import ArgumentParser
import json 
import relationships
import sys

class Person():
    """ Represents a person in a family. 
    
        Attributes: 
            name (str): A person's name. 
            gender (str): the person’s gender. It should have one of the following values: 'f', 'm', 'n'.
            parents (list of Person objects): The person’s parents, if known (a list of instances of Person; may be empty).
            spouse (Person): the person's spouse, if applicable (an instance of Person, or None).
    """
    def __init__(self, name, gender):
        """Create attributes for Person class.
        Args:
            name (str): the persons name.
            gender (str): The persons gender, should have one of the following values: 'f', 'm', 'n'.
            
        Side effects: 
            Creates the atributes of name, gender, parnets, and spouse for Person class.
        """
        self.name = name
        self.gender = gender
        self.parents = []
        self.spouse = None
 

    def add_parent(self, person):
        """This method adds a parent to the person class
        
            Side effects: 
                Modifies the self.parents by adding to the a person list.
        """
        self.person = person
        self.parents.append(self.person)

    def set_spouse(self, person):
        """This method adds a spouse.
        """
        self.person = person
        """
        Create an attribute for self 
        """
        self.spouse = self.person

    def connections(self):
        """ Finds connections to relatives.
        Returns:
            cdict: a dictionary of connections
        """
        cdict = {self: ""} 
        queue = [self]
        while queue: 
            person = queue.pop(0) 
            personpath = cdict[person]
            
            for parent in person.parents: 
                if parent not in cdict: 
                    path_to_parent = personpath + "P"
                    cdict[parent] = path_to_parent 
                    queue.append(parent)
                    
            if 'S' not in personpath and person.spouse and person.spouse not in cdict: 
                path_to_spouse = personpath + "S"
                cdict[person.spouse] = path_to_spouse
                queue.append(person.spouse)
        return cdict
                
    def relation_to(self, person):
        """Finds people's relations
        Args:
            person (Person): An instance of the Person class.
        Returns:
            str: realtionship between the two individuals.

        """
        dict_person = person.connections()
        dict_self = self.connections()
        shared_keys = set(dict_self).intersection(set(dict_person))

        if not shared_keys:
            return None
        else:
            lcr = min(shared_keys, key = lambda p: len(f"{dict_self[p]} : {dict_person[p]}"))
            lcr_path = f"{dict_self[lcr]}:{dict_person[lcr]}"
            if lcr_path in relationships.relationships: 
                return relationships.relationships[lcr_path][self.gender]
            else: 
                return "distant relative" 

class Family():
    """ Keeps track of the Person instances created.
    
    Attributes: 
        people (dict): they keys are people and the objects are who they are related to.
        """
    def __init__(self, dict):
        """Creates empty dictionary
        Args:
            dict (dict): dictionary storing names and relatives:
            individuals (dict) - Name and gender of an individual.
            parents (dict) - A persons name and their parent.
            couples (list of str) - Two people who are married.
            
        Side Effects: 
            Creates the people attribute, modifies the parent and spouse attributes.
        """
        self.people = {}
        for name, gender in dict['individuals'].items():
            person = Person(name, gender)
            self.people[name] = person

        for person in dict['parents']:
            pers_object = self.people[person]
            for parent in dict ['parents'][person]:
                parent_person = self.people[parent]
                pers_object.add_parent(parent_person)
            

        for pair in dict['couples']:
            first_person = self.people[pair[0]]
            second_person = self.people[pair[1]]
            first_person.set_spouse(second_person)
            second_person.set_spouse(first_person)

    def relation(self, name1, name2):
        """Returns the calculated relationship between two individuals.
        Args:
            name1 (str): Persons name
            name2 (str): Second persons name
        Returns:
            None or (str): a kinship term
        """
        object_name1 = self.people[name1]
        object_name2 = self.people[name2]

        return object_name1.relation_to(object_name2)
    
def main(json_path, person_name, person2_name):
    """Loads file to determine peoples relations.
    Args:
        json_path (str): The path to the JSON file.
        person_name (str): The first persons name in the JSON file.
        person2_name (str): The second person's name in the JSON file.
        
    Side effects: 
        Prints
    """
    with open(json_path, "r", encoding="utf-8") as f:
        familydata = json.load(f)
        family_inst = Family(familydata)
        related = family_inst.relation(person_name, person2_name)
        if related == None:
            print(f"{person_name} is not related to {person2_name}")
        else:
            print(f"{person_name} is {person2_name}'s " + related)

def parse_args(args):
    """Parse commandline arguments.
    Args:
        args(list of str): commandline arguments.
    Returns:
        A namespace: The namespace object.
    """
    parser = ArgumentParser()
    parser.add_argument("filepath", help = "The filepath of the json file")
    parser.add_argument("name1", help = "The first name in the json file")
    parser.add_argument("name2", help = "The second name in the json file")

    return parser.parse_args(args)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.filepath, args.name1, args.name2)





