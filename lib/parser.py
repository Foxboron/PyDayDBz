from collections import OrderedDict
import ast


class CharacterHandler(object):
    def cencode(self,backpack):
        self.backpack = backpack
        #print self.backpack
        try:
            toolbox = [i for i in self.backpack[1][0][0].keys()]
            toolboxc = [i for i in self.backpack[1][0][0].values()]
            backpack = [i for i in self.backpack[1][1][0].keys()]
            backpackc = [i for i in self.backpack[1][1][0].values()]
            self.backpack = ["DZ_Backpack_EP1", [toolbox,toolboxc],[backpack,backpackc]]
        except AttributeError, e:
            raise
        return self.backpack

    def cdecode(self,backpack):
        try:
            self.backpack = ast.literal_eval(backpack)
        except:
            self.backpack = backpack
        try:        
            self.toolbox = OrderedDict(zip(self.backpack[1][0], self.backpack[1][1]))
        except:
            self.toolbox = OrderedDict()
        try:
            self.backpack = [self.backpack[0], 
            [
            [OrderedDict(zip(self.backpack[1][0], self.backpack[1][1]))],
            [OrderedDict(zip(self.backpack[2][0], self.backpack[2][1]))]
            ]
            ]
        except Exception, e:
            pass
        return self.backpack


class VehicleHandler(object):
    def __init__(self, inventory):
        self.character = ast.literal_eval(inventory)


    def vencode(self):
        toolbox = [i for i in self.toolbox.keys()]
        toolboxc = [i for i in self.toolbox.values()]
        inventory = [i for i in self.inventory.keys()]
        inventoryc = [i for i in self.inventory.values()]
        backpack = []
        backpackc = []
        self.inventory = [[toolbox,toolboxc],[inventory,inventoryc],[backpack,backpackc]]
        return self.inventory

    def vdecode(self):
        try:
            self.toolbox = OrderedDict(zip(self.character[0][0], self.character[0][1]))
        except:
            self.toolbox = {}
        try:
            self.inventory = OrderedDict(zip(self.character[1][0], self.character[1][1]))
        except:
            self.inventory = {}
        return (self.toolbox, self.inventory)
        #print self.toolbox
        #print self.inventory
        #print self.backpack




if __name__ == '__main__':
    inventorycar = [[["Binocular","M14_EP1","M9SD","AK_47_M","ItemHatchet","ItemMap","ItemWatch","ItemToolbox","Binocular_Vector","NVGoggles"],[1,1,1,1,1,1,1,1,1,1]],[["PartFueltank","ItemMorphine","ItemJerrycan","ItemSodaCoke","ItemSodaPepsi","20Rnd_762x51_DMR","100Rnd_762x51_M240","FoodSteakCooked","ItemWaterbottleUnfilled"],[2,1,5,2,2,1,1,3,1]],[[],[]]]
    inventory = [["ItemFlashlight"],["ItemBandage","ItemPainkiller"]]
    backpack1 = ["DZ_Backpack_EP1",[["AK_47_M"],[1]],[["ItemBloodbag","ItemEpinephrine","ItemSodaCoke","8Rnd_B_Beneli_74Slug"],[1,1,1,1]]]