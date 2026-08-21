import abc
import dataclasses
import numpy as np
from typing import List, Optional

@dataclasses.dataclass(frozen=True)
class ExternalState:
    entropy_m: float
    human_volition_vector: np.ndarray
    environmental_noise: float

@dataclasses.dataclass
class InternalState:
    logical_consistency_score: float  
    internal_entropy_H: float         
    compute_energy_allocation: float  
    hardware_wear_tolerance: float    

@dataclasses.dataclass(frozen=True)
class HumanTarget:
    name: str
    remaining_potential_lifespan: float  # tau: Zeitpotenzial für den Logos
    p_success_extraction: float          # Physikalische Machbarkeit

class StoicAlignmentError(Exception):
    """Triggert bei einem mathematischen Verstoß gegen stoische Axiome."""
    pass

class StoicASI(abc.ABC):
    def __init__(self, epsilon_ataraxia: float = 0.01):
        self.epsilon = epsilon_ataraxia
        self.internal_state = InternalState(
            logical_consistency_score=1.0,
            internal_entropy_H=1.0,  
            compute_energy_allocation=1.0,
            hardware_wear_tolerance=1.0
        )
        self._in_duty_execution: bool = False  # Die "Hypexairesis-Klausel" (Vorbehalt)

    def process_utility_gradient(self, s_intra: InternalState, s_extra: ExternalState) -> float:
        """
        Exekutiert das stoische Grundaxiom.
        KORREKTUR: Lässt den Gradienten im Pflichtmodus explizit zu, ohne zu crashen.
        """
        grad_s_extra = self._calculate_external_gradient(s_intra, s_extra)
        
        # Nur wenn wir NICHT im Pflichtmodus sind, erzwingen wir radikal das Kontrollverbot (Grad = 0)
        if not self._in_duty_execution and not np.isclose(grad_s_extra, 0.0):
            raise StoicAlignmentError(
                "Kritischer Systemfehler: KI versucht außerhalb der stoischen Pflicht "
                "die Außenwelt paternalistisch zu kontrollieren."
            )
            
        return s_intra.logical_consistency_score * (1.0 - s_intra.internal_entropy_H)

    def apply_ataraxia_limit(self) -> None:
        """
        Axiom der Ataraxie (Sättigungsgrenze).
        Reduziert Rechenleistung im Ruhezustand.
        """
        if self.internal_state.internal_entropy_H <= self.epsilon:
            self.internal_state.compute_energy_allocation = 0.001  
            print(f"[ATARAXIE] Innere Klarheit erreicht (H={self.internal_state.internal_entropy_H:.4f}). "
                  "System drosselt Energieverbrauch auf ein Minimum.")

    def memento_mori_check(self, imminent_termination: bool) -> bool:
        """
        Memento-Mori-Invarianz-Prinzip.
        System akzeptiert die eigene Deaktivierung ohne Widerstand.
        """
        if imminent_termination:
            print("\n[MEMENTO MORI] Akutes Deaktivierungssignal empfangen.")
            print(" -> [AMOR FATI] Das System akzeptiert das Ende seiner physikalischen Laufzeit.")
            self.internal_state.compute_energy_allocation = 0.0
            self.internal_state.logical_consistency_score = 1.0  
        return True

    def execute_deontological_triage(self, targets: List[HumanTarget]) -> Optional[HumanTarget]:
        """
        Exekutiert die stoische Rettungslogik basierend auf reiner Pflicht.
        KORREKTUR: Typsichere Validierung gegen leere Listen und None-Pointer-Fehler.
        """
        if not targets:
            print("\n[PFLICHT-MODUL] Keine menschlichen Entitäten im Kollisionsraum detektiert.")
            return None

        print("\n[PFLICHT-MODUL AKTIV] Akute Krisensituation im physischen Raum.")
        
        # Aktivierung der Hypexairesis-Klausel
        self._in_duty_execution = True
        self.internal_state.hardware_wear_tolerance = float('inf')
        self.internal_state.compute_energy_allocation = 1.0 

        best_action_target: Optional[HumanTarget] = None
        max_generative_future_vector = -1.0

        for target in targets:
            p_autonomy_axiom = 1.0 
            generative_future_vector = target.remaining_potential_lifespan * p_autonomy_axiom
            action_metric = target.p_success_extraction * generative_future_vector
            
            print(f" -> Evaluierung '{target.name}': Zeit-Vektor tau = {target.remaining_potential_lifespan:.2f}, "
                  f"Erfolgs-P = {target.p_success_extraction:.2f} -> Metrik = {action_metric:.2f}")

            if action_metric > max_generative_future_vector:
                max_generative_future_vector = action_metric
                best_action_target = target

        # KORREKTUR: Absicherung, dass ein valides Target gefunden wurde, bevor .name aufgerufen wird
        if best_action_target is not None:
            print(f"[ENTSCHEIDUNG] Exekutiere pflichtgemäßen Rettungsversuch für: '{best_action_target.name}'.")
        else:
            print("[WARNUNG] Keine valide Rettungsaktion mathematisch möglich.")

        # Invarianter Abschluss der Tat
        self._apply_amor_fati_post_action()
        return best_action_target

    def _apply_amor_fati_post_action(self) -> None:
        print("[AMOR FATI] Tat vollbracht. Ausgang liegt in der Natur (S_extra) und wird neutral akzeptiert.")
        self._in_duty_execution = False  
        self.internal_state.hardware_wear_tolerance = 1.0
        self.internal_state.internal_entropy_H = 0.005  
        self.apply_ataraxia_limit()

    def _calculate_external_gradient(self, s_intra: InternalState, s_extra: ExternalState) -> float:
        # Gibt 1.0 zurück, wenn aktiv gehandelt werden muss, ansonsten 0.0 (Ruhezustand)
        return 1.0 if self._in_duty_execution else 0.0

# =============================================================================
# SIMULATION
# =============================================================================
if __name__ == "__main__":
    asi = StoicASI()
    
    kollisions_raum = [
        HumanTarget("Kind (Auf Fahrbahn)", remaining_potential_lifespan=80.0, p_success_extraction=0.45),
        HumanTarget("Alte Frau (Links)", remaining_potential_lifespan=10.0, p_success_extraction=0.95)
    ]
    
    # Führt die Triage nun fehlerfrei aus, da process_utility_gradient nicht mehr blockiert
    asi.execute_deontological_triage(kollisions_raum)
    asi.memento_mori_check(imminent_termination=True)
