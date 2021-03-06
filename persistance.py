#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
# Lopez Aliaume
# 30/03/2013
# 
# Fichier gérant tout ce qui est persistance 
# des informations dans une sorte de BDD
# 
# 
# L'API est orientée vers les clé => valeur
# et laisse le soin à l'utilisateur de définir
# son propre fonctionnement : il n'y a pas 
# de schémas prédéfinis d'utilisation !
#
#
# BDD :
# [ 
#	["fichier1", ["variable1", "valeur1"], ... , ["variableN","valeurN"]],
#	...
#	["fichierN", ["variable1", "valeur1"], ... , ["variableN","valeurN"]]
# ]
	


# ma variable globale : BDD
persistant = []

def liste_fichiers ():
	""" Retourne les fichiers chargés
		
		@return : [string ...]
	"""
	l = []
	for i in persistant:
		l.append (i[0])
	return l
	
def liste_variables (fichier):
	""" Retourne toutes les variables dans un fichier
	
		@fichier : string = nom du fichier dans lequel chercher les variables
		
		@return : [string ...]
	"""
	l = False
	for i in persistant:
		if i[0] == fichier:
			l = []
			for j in i[1:]:
				l.append (j[0])
			break
	return l

def charger_fichier (chemin):
	""" Charge un fichier de configuration
		
		@chemin : string = chemin du fichier à charger
		
		@return : bool = si ça s'est bien passé 
	"""
	global persistant 
	try:
		f = open (chemin,"r")
		newlist = [chemin]
	
		for line in f:
			if line != "\n" and line[0] != "#":
				s = line[:-1].replace ("\\n","\n").split (" |=> ")
				newlist.append (s)
		
		persistant.append (newlist)
		return True
	except:
		return False
	
def get_propriete (chemin,nom):
	""" Récupère une propriété
		
		@chemin : string = chemin du fichier dans lequel se trouve la propriété
		@nom : string = nom de la propriété 
		
		@return : string | False
	"""
	for p in persistant:
		if p[0] == chemin:
			for i in p[1:]:
				if i[0] == nom:
					return i[1]
			break
	
	return False

def get_by_value (chemin,val):
	""" Récupère le nom de la propriété contenant la valeur @val
		
		@chemin : string = chemin du fichier dans lequel se trouve la propriété
		@val : string = valeur de la propriété
		
		@return : string | False
	"""
	for p in persistant:
		if p[0] == chemin :
			for i in p[1:]:
				if i[1] == val:
					return i[0]
			break
	return False
	
def new_file (chemin):
	""" Ajoute un fichier virtuel (enregistré plus tard)
		
		@chemin : string = chemin du fichier à créer 
		
		@return : None
	"""
	global persitant
	# TODO:
	# vérification de la préexistance du fichier ... 
	persistant.append ([chemin])
	
def add_propriete (chemin,nom,val):
	""" Ajoute une propriété, même si elle existe déjà
		
		@chemin : string = chemin du fichier dans lequel se trouve la propriété
		@nom : string = nom de la propriété
		@val : string = valeur de la propriété  
		
		@return : bool = si ça s'est bien passé 
	"""
	global persistant 
	
	for p in persistant:
		if p[0] == chemin:
			p.append ([nom,val])
			return True
	return False

def set_propriete (chemin,nom,val):
	""" Définit une propriété, et la crée si elle n'existe pas 
		
		@chemin : string = chemin du fichier dans lequel se trouve la propriété
		@nom : string = nom de la propriété
		@val : string = valeur de la propriété  
		
		@return : bool = si ça s'est bien passé 
	"""
	global persistant
	
	for p in persistant:
		if p[0] == chemin:
			for i in p[1:]:
				if i[0] == nom:
					i[1] = val
					return True
			p.append ([nom,val])
			return True
	return False
	
def save ():
	""" Enregistre les modifications dans les fichiers
	
		@return : bool = si ça s'est bien passé 
	"""
	try:
		for p in persistant:
			f = open (p[0],"w")
			for prop in p[1:]:
				f.write (prop[0] + " |=> " + prop[1].replace ("\n","\\n"))
				f.write ("\n")
			f.close ()
	except:
		return False
		
def init ():
	""" fonction d'initialisation du module
	
		@return : None 
	"""
	
	# fichier de configuration globale
	a = charger_fichier ("config")
	
	# fichier des scores 
	b = charger_fichier ("scores")
	
	# fichier des couleurs
	c = charger_fichier ("couleurs")
	
	if a and b and c: # si les trois ont été chargés 
		return True
	else:
		return False
		
